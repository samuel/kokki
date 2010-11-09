
import os
from kokki import *

env.include_recipe("boto")

# Mount volumes and format is necessary

for vol in env.config.aws.volumes:
    env.cookbooks.aws.EBSVolume(vol.get('name') or vol['volume_id'],
        volume_id = vol.get('volume_id'),
        availability_zone = env.config.aws.availability_zone,
        device = vol['device'],
        action = "attach" if vol['volume_id'] else ["create", "attach"])

    if vol.get('fstype'):
        if vol['fstype'] == "xfs":
            Package("xfsprogs")
        Execute("mkfs.%(fstype)s -f %(device)s" % vol,
            not_if = """if [ "`file -s %(device)s`" = "%(device)s: data" ]; then exit 1; fi""" % vol)

    if vol.get('mount_point'):
        Mount(vol['mount_point'],
            device = vol['device'],
            fstype = vol.get('fstype'),
            options = vol.get('fsoptions', ["noatime"]),
            action = ["mount", "enable"])
