
from kokki import *

env.include_recipe("java.jre")

apt_list_path = '/etc/apt/sources.list.d/cloudera.list'
apt = (
    "deb http://archive.cloudera.com/debian {distro}-cdh3 contrib\n"
    "deb-src http://archive.cloudera.com/debian {distro}-cdh3 contrib\n"
).format(distro=env.system.lsb['codename'])

Execute("apt-update-clouders",
    command = "apt-get update",
    action = "nothing")

Execute("curl -s http://archive.cloudera.com/debian/archive.key | sudo apt-key add -",
    not_if = "(apt-key list | grep Cloudera > /dev/null)")

File(apt_list_path,
    owner = "root",
    group ="root",
    mode = 0644,
    content = apt,
    notifies = [("run", env.resources["Execute"]["apt-update-clouders"], True)])
