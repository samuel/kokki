
from kokki import Execute, File, Fail

apt_list_path = '/etc/apt/sources.list.d/librato.list'
apt = None
if env.system.platform == "ubuntu":
    ver = env.system.lsb['release']
    if ver == "10.04":
        apt = "deb http://apt.librato.com/ubuntu/ lucid non-free"
    elif ver in ("10.10", "11.04", "11.10"):
        apt = "deb http://apt.librato.com/ubuntu/ maverick non-free"
elif env.system.platform == "debian":
    ver = env.system.lsb['release']
    if ver == '5.0':
        apt = "deb http://apt.librato.com/debian/ lenny non-free"

if not apt:
    raise Fail("Can't find a librato package for your platform/version")

Execute("apt-update-librato",
    command = "apt-get update",
    action = "nothing")

Execute("curl http://apt.librato.com/packages.librato.key | apt-key add -",
    not_if = "(apt-key list | grep Librato > /dev/null)")

File(apt_list_path,
    owner = "root",
    group ="root",
    mode = 0644,
    content = apt+"\n",
    notifies = [("run", env.resources["Execute"]["apt-update-librato"], True)])
