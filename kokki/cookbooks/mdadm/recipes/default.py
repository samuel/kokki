
from kokki import Package, Execute, Mount

if env.config.mdadm.arrays:
    Package("mdadm")

Execute("mdadm-update-conf",
    action = "nothing",
    command = ("("
        "echo DEVICE partitions > /etc/mdadm/mdadm.conf"
        "; mdadm --detail --scan >> /etc/mdadm/mdadm.conf"
    ")"
    ))

for arr in env.config.mdadm.arrays:
    array = arr.copy()
    fstype = array.pop('fstype', None)
    fsoptions = array.pop('fsoptions', None)
    mount_point = array.pop('mount_point', None)

    env.cookbooks.mdadm.Array(**array)

    if fstype:
        if fstype == "xfs":
            Package("xfsprogs")
        Execute("mkfs.%(fstype)s -f %(device)s" % dict(fstype=fstype, device=array['name']),
            not_if = """if [ "`file -s %(device)s`" = "%(device)s: data" ]; then exit 1; fi""" % dict(device=array['name']))

    if mount_point:
        Mount(mount_point,
            device = array['name'],
            fstype = fstype,
            options = fsoptions if fsoptions is not None else ["noatime"],
            action = ["mount", "enable"])
