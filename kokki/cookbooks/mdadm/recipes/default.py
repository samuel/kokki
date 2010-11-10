
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
    env.cookbooks.mdadm.Array(**array,
        notifies = [("run", env.resources["Execute"]["mdadm-update-conf"])])
