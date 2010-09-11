
import urllib2
from kokki import *

def get_ec2_metadata(key):
    res = urllib2.urlopen("http://169.254.169.254/2008-02-01/meta-data/" + key)
    return res.read().strip()

def setup():
    env.set_attributes({
        'aws.instance_id': get_ec2_metadata('instance-id'),
        'aws.instance_type': get_ec2_metadata('instance-type'),
        'aws.availability_zone': get_ec2_metadata('placement/availability-zone'),
    }, overwrite=True)
setup()

Package("python-boto")

# Mount volumes and format is necessary

Package("xfsprogs")

for vol in env.aws.volumes:
    cookbooks.aws.EBSVolume(vol['volume_id'],
        availability_zone = env.aws.availability_zone,
        device = vol['device'],
        action = "attach")

    if vol.get('fstype'):
        Execute("mkfs.%(fstype)s -F %(device)s" % vol,
            not_if = """if [ "`file -s %(device)s`" = "%(device)s: data" ]; then exit 1; fi""" % vol)

    if vol.get('mount_point'):
        Mount(vol['mount_point'],
            device = vol['device'],
            fstype = vol.get('fstype'),
            options = vol.get('fsoptions', ["noatime"]),
            action = ["mount", "enable"])
