$TTL 3600
@    IN    SOA    gnome3.com. hostmaster.gnome.org.  (
                2022041500 ; Serial
                28800      ; Refresh
                14400      ; Retry
                1000000    ; Expire
                21600 )    ; Minimum

    IN    NS    ns-master.gnome.org.
    IN    NS    ns-slave.gnome.org.
    IN    MX    10    smtp.gnome.org.

    IN  A   8.43.85.3    
    IN  A   8.43.85.4
    IN  A   8.43.85.5

www IN  CNAME    router-default.apps.openshift4.gnome.org.
