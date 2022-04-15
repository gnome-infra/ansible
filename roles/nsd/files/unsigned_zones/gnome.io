$TTL 300
@        IN    SOA    ns-master.gnome.org. hostmaster.gnome.org. (
                2021011800; Serial
                28800; Refresh
                7200; Retry
                604800; Expire
                300; Default TTL
                )

                IN    NS    ns-master.gnome.org.
                IN    NS    ns-slave.gnome.org.

                MX  10  smtp.gnome.org. 

                IN  A   8.43.85.3
                IN  A   8.43.85.4
                IN  A   8.43.85.5

www IN  CNAME    router-default.apps.openshift4.gnome.org.
