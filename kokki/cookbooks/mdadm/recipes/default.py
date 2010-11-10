
from kokki import *

if env.config.mdadm.arrays:
    Package("mdadm")

Execute("mdadm-update-conf",
    action = "nothing",
    command = "mdadm --detail --scan >> /etc/mdadm/mdadm.conf")

for array in env.config.mdadm.arrays:
    Execute("mdadm-create-" + array['name'],
        creates = array['name']
        command = "mdadm --create {name} -R -c {chunksize} --level {level} --metadata={metadata} --raid-devices {device_count} {devices}".format(
            name = array['name'],
            chunksize = array['chunksize'],
            level = array['level'],
            metadata = array['metadata'],
            device_count = len(array['devices']),
            " ".join(array['devices']),
        ),
        notifies = [("run", env.resources["Execute"]["mdadm-update-conf"])])
