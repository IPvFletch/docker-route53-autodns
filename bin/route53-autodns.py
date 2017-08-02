#!/usr/bin/python
#
# Usage: python /bin/route53-autodns.py <hostname>
#

import os
import sys
import boto
import requests

from boto.route53.record import ResourceRecordSets


def get_zone_id(hostname):
  domainname = '.'.join(hostname.split('.')[-2:])
  zone = conn.get_hosted_zone_by_name(domainname)
  if not zone:
    print "Domain not available!"
    exit(1)
  return zone.GetHostedZoneResponse.Id.split('/')[2]


def get_local_ip():
  return requests.get("http://169.254.169.254/latest/meta-data/local-ipv4").content


def register(hostname, ip, ttl):
  changes = ResourceRecordSets(conn, zone_id)
  change = changes.add_change('UPSERT', hostname, 'A', ttl)
  change.add_value(ip)
  print 'Updated %s with IP %s' % (hostname, ip)
  return changes.commit()


if len(sys.argv) < 1:
    print 'Usage: python route53-autodns <hostname>'
    exit(1)

hostname = sys.argv[1] + '.' + os.environ.get('DOMAINNAME')

conn = boto.connect_route53(os.environ.get('AWS_ACCESS_KEY'), os.environ.get('AWS_SECRET_KEY'))
zone_id = get_zone_id(hostname)

result_local = register(hostname, get_local_ip(), 300)
if not result_local:
  print 'ERROR: Could not upsert DNS for %s' % hostname
  exit(1)

sys.stdout.flush()
