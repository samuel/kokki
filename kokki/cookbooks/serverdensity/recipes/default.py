
from kokki import *

apt_list_path = '/etc/apt/sources.list.d/serverdensity.list'
apt = None
if env.system.platform == "ubuntu":
    ver = env.system.lsb['release']
    apt = "deb http://www.serverdensity.com/downloads/linux/debian lenny main"
    # if ver == "10.04":
    #     apt = "deb http://apt.librato.com/ubuntu/ lucid non-free"
elif env.system.platform == "debian":
    ver = env.system.lsb['release']
    apt = "deb http://www.serverdensity.com/downloads/linux/debian lenny main"
    # if ver == '5.0':
    #     apt = "deb http://apt.librato.com/debian/ lenny non-free"

if not apt:
    raise Fail("Can't find a mongodb package for your platform/version")

Execute("apt-update-serverdensity",
    command = "apt-get update",
    action = "nothing")

Execute("curl http://www.serverdensity.com/downloads/boxedice-public.key | apt-key add -",
    not_if = "(apt-key list | grep 'Server Density' > /dev/null)")

File(apt_list_path,
    owner = "root",
    group ="root",
    mode = 0644,
    content = apt+"\n",
    notifies = [("run", env.resources["Execute"]["apt-update-serverdensity"], True)])

Package("sd-agent")

File("/etc/sd-agent/config.cfg",
    content = Template("serverdensity/config.cfg.j2"))
