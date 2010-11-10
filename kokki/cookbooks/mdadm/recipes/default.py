
from kokki import *

if env.config.mdadm.arrays:
    Package("mdadm")

Execute("mdadm-update-conf",
    action = "nothing",
    command = ("("
        "echo DEVICE partitions > /etc/mdadm/mdadm.conf"
        "; mdadm --detail --scan >> /etc/mdadm/mdadm.conf"
    ")"
    ))

for array in env.config.mdadm.arrays:
    env.cookbooks.mdadm.Array(notifies = [("run", env.resources["Execute"]["mdadm-update-conf"])], **array)

    if array.get('fstype'):
        if array['fstype'] == "xfs":
            Package("xfsprogs")
        Execute("mkfs.%(fstype)s -f %(device)s" % dict(fstype=array['fstype'], device=array['name']),
            not_if = """if [ "`file -s %(device)s`" = "%(device)s: data" ]; then exit 1; fi""" % dict(device=array['name']))

    if array.get('mount_point'):
        Mount(array['mount_point'],
            device = array['name'],
            fstype = array['fstype'],
            options = array['fsoptions'] if array.get('fsoptions') is not None else ["noatime"],
            action = ["mount", "enable"])
