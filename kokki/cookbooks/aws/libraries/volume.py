
from kokki import *

def setup_ebs_volume(name=None, availability_zone=None, volume_id=None, device=None, snapshot_id=None, size=None, fstype=None, mount_point=None, fsoptions=None):
    env = Environment.get_instance()

    env.cookbooks.aws.EBSVolume(name or volume_id,
        volume_id = volume_id,
        availability_zone = availability_zone or env.config.aws.availability_zone,
        device = device,
        snapshot_id = snapshot_id,
        size = size,
        action = "attach" if volume_id else ["create", "attach"])

    if fstype:
        if fstype == "xfs":
            Package("xfsprogs")
        Execute("mkfs.%(fstype)s -f %(device)s" % dict(fstype=fstype, device=device),
            not_if = """if [ "`file -s %(device)s`" = "%(device)s: data" ]; then exit 1; fi""" % dict(device=device))

    if mount_point:
        Mount(mount_point,
            device = device,
            fstype = fstype,
            options = fsoptions if fsoptions is not None else ["noatime"],
            action = ["mount", "enable"])
