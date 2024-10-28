#!/usr/bin/env python3

import subprocess
import argparse
import sys
import ldap
from datetime import datetime

class IPALDAPMonitor:
    def __init__(self):
        self.IPA_CTL = "/sbin/ipactl"
        self.VERSION = "1.0.0"
        self.METRICS_FILE = "/var/lib/node_exporter/textfile_collector/ipa_ldap_status.prom"

    def get_ipa_status(self, verbose=False):
        try:
            cmd = [self.IPA_CTL, "status"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()

            if verbose:
                print("[V]: Output of ipactl status:")
                print(stdout)

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd, stderr)

            return self._parse_status_output(stdout)

        except subprocess.CalledProcessError as e:
            return None, str(e)

    def _parse_status_output(self, output):
        services = {}
        for line in output.splitlines():
            if 'must be running' in line:
                continue
            parts = line.split()
            if len(parts) >= 3:
                service_name = parts[0]
                status = parts[2]
                services[service_name] = status == "RUNNING"
        return services, None

    def get_ldap_replication_status(self, uri="ldaps://localhost:636", bind_dn=None, bind_pw=None):
        try:
            l = ldap.initialize(uri)
            if bind_dn:
                l.bind_s(bind_dn, bind_pw)

            replication = l.search_s('cn=config',
                ldap.SCOPE_SUBTREE,
                '(objectclass=nsds5replicationagreement)',
                ['nsDS5ReplicaHost', 'nsds5replicaLastUpdateStatus'])

            replica_status = {}
            for rhost in replication:
                host = rhost[1]['nsDS5ReplicaHost'][0].decode()
                status_code = rhost[1]['nsds5replicaLastUpdateStatus'][0].decode()
                if "Success" in status_code:
                    status_code = '0'
                elif "Error" in status_code:
                    status_code = '2'
                else:
                    status_code = '1'
                replica_status[host] = status_code

            return replica_status, None

        except Exception as e:
            return None, str(e)

    def write_prometheus_metrics(self, services, replica_status, ipa_error=None, ldap_error=None):
        with open(self.METRICS_FILE, 'w') as f:
            # IPA Service Status Metrics
            f.write("""# HELP ipa_service_status Status of IPA services (1=running, 0=not running)
# TYPE ipa_service_status gauge
""")
            if services:
                for service, is_running in services.items():
                    f.write(f'ipa_service_status{{service="{service}"}} {1 if is_running else 0}\n')

            f.write("""
# HELP ipa_status_ok Whether all IPA services are running (1=all running, 0=some not running)
# TYPE ipa_status_ok gauge
""")
            if services:
                all_running = all(services.values())
                f.write(f'ipa_status_ok {1 if all_running else 0}\n')
            else:
                f.write('ipa_status_ok 0\n')

            # LDAP Replication Metrics
            f.write("""
# HELP ldap_replica_status Status of LDAP replication (0=success, 1=busy, 2=error)
# TYPE ldap_replica_status gauge
""")
            if replica_status:
                for host, status in replica_status.items():
                    f.write(f'ldap_replica_status{{host="{host}"}} {status}\n')

            f.write("""
# HELP ldap_replica_count Total number of LDAP replicas
# TYPE ldap_replica_count gauge
""")
            replica_count = len(replica_status) if replica_status else 0
            f.write(f'ldap_replica_count {replica_count}\n')

            # Error Metrics
            f.write("""
# HELP ipa_check_error Whether there was an error checking IPA status (1=error, 0=no error)
# TYPE ipa_check_error gauge
""")
            f.write(f'ipa_check_error {1 if ipa_error else 0}\n')

            f.write("""
# HELP ldap_check_error Whether there was an error checking LDAP replication (1=error, 0=no error)
# TYPE ldap_check_error gauge
""")
            f.write(f'ldap_check_error {1 if ldap_error else 0}\n')

            if ipa_error:
                f.write(f'ipa_check_error_info{{error="{ipa_error}"}} 1\n')
            if ldap_error:
                f.write(f'ldap_check_error_info{{error="{ldap_error}"}} 1\n')

            # Timestamp
            f.write("""
# HELP ipa_ldap_check_timestamp_seconds Timestamp of last check
# TYPE ipa_ldap_check_timestamp_seconds gauge
""")
            f.write(f'ipa_ldap_check_timestamp_seconds {int(datetime.now().timestamp())}\n')

def main():
    parser = argparse.ArgumentParser(description='IPA and LDAP status checker for Node Exporter')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    parser.add_argument('-V', '--version', action='store_true', help='Show version information')
    parser.add_argument('-u', '--ldap-uri', default='ldaps://localhost:636', help='LDAP URI')
    parser.add_argument('-D', '--bind-dn', help='Bind DN')
    parser.add_argument('-w', '--bind-password', help='Bind Password')
    args = parser.parse_args()

    monitor = IPALDAPMonitor()

    if args.version:
        print(f"IPA LDAP Monitor {monitor.VERSION}")
        sys.exit(0)

    # Get IPA status
    services, ipa_error = monitor.get_ipa_status(args.verbose)

    # Get LDAP replication status
    replica_status, ldap_error = monitor.get_ldap_replication_status(
        args.ldap_uri, args.bind_dn, args.bind_password
    )

    # Write all metrics
    monitor.write_prometheus_metrics(services, replica_status, ipa_error, ldap_error)

    if args.verbose:
        if ipa_error or ldap_error:
            print(f"UNKNOWN: IPA Error: {ipa_error}, LDAP Error: {ldap_error}")
            sys.exit(3)
        elif not replica_status:
            print("WARNING: No replicas found")
            sys.exit(1)
        elif services and all(services.values()) and all(s in ['0', '1'] for s in replica_status.values()):
            print("OK: All services running and replication healthy")
            sys.exit(0)
        else:
            not_running = [svc for svc, status in services.items() if not status]
            failed_replicas = [host for host, status in replica_status.items() if status not in ['0', '1']]
            print(f"CRITICAL: Services not running: {', '.join(not_running)}, Failed replicas: {', '.join(failed_replicas)}")
            sys.exit(2)

if __name__ == "__main__":
    main()
