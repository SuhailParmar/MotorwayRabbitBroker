#!/usr/bin/bash
# Create vHost    user:pass         host port       vhost_name
curl -i -X PUT -u guest:guest "http://localhost:15672/api/vhosts/motorway_vhost"

#curl -i -X PUT -u ${1}:${2} "http://${3}:${4}/api/vhosts/${5}"