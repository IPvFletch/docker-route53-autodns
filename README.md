# Docker Route53 AutoDNS

Registers container Hostnames in AWS Route53 using the local EC2 Instance IP address.
The EC2 Instance Meta-Data is used to determine the local IPv4 IP address.

This script requires 3 ENV variables:
  * DOMAINNAME
  * AWS_ACCESS_KEY
  * AWS_SECRET_KEY

$DOMAINNAME is automatically appended to the container Hostname, ex. container.domain.name.

# Usage
    python route53-autodns.py <hostname>

# Notes
  When used with docker-gen, a list of container Hostnames is created based on a template (ex. route53.tmpl).
  Docker-gen then executes the output (ex. /bin/bash /tmp/route53.sh) which runs this script using the hostname list.
  Only publishes DNS for containers which have the HOSTNAME ENV var set.
