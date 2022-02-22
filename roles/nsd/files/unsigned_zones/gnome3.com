$TTL 3600
@    IN    SOA    gnome3.com. hostmaster.gnome.org.  (
                2021011800 ; Serial
                28800      ; Refresh
                14400      ; Retry
                1000000    ; Expire
                21600 )    ; Minimum

    IN    NS    ns-master.gnome.org.
    IN    NS    ns-slave.gnome.org.
    IN    MX    10    smtp.gnome.org.

    IN  A   8.43.85.13    
    IN  A   8.43.85.14
    IN  A   8.43.85.29

www IN  CNAME    openshift.gnome.org.
