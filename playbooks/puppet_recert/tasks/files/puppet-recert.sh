#!/bin/bash

service puppet stop

find /var/lib/puppet/ssl -type f -exec rm -f "{}" \;

puppet agent --test --server puppetmaster.gnome.org --ca_server puppetmaster01.gnome.org

service puppet restart
