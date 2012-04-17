
from kokki import Execute, Fail, File, Template, Package, Service

assert env.config.cloudkick.oauth_key and env.config.cloudkick.oauth_secret and env.config.cloudkick.hostname

apt_list_path = '/etc/apt/sources.list.d/cloudkick.list'
apt = None
if env.system.platform == "ubuntu":
    ver = env.system.lsb['release']
    if ver in ("10.10", "11.04", "11.10"):
        apt = "deb http://packages.cloudkick.com/ubuntu maverick main"
    elif ver == "10.04":
        apt = "deb http://packages.cloudkick.com/ubuntu lucid main"
    elif ver == "9.10":
        apt = "deb http://packages.cloudkick.com/ubuntu karmic main"
    elif ver == "9.04":
        apt = "deb http://packages.cloudkick.com/ubuntu jaunty main"
    elif ver == "8.10":
        apt = "deb http://packages.cloudkick.com/ubuntu intrepid main"
    elif ver == "8.04":
        apt = "deb http://packages.cloudkick.com/ubuntu hardy main"
    elif ver == "6.04":
        apt = "deb http://packages.cloudkick.com/ubuntu dapper main"
elif env.system.platform == "debian":
    ver = env.system.lsb['release']
    apt = "deb http://packages.cloudkick.com/ubuntu lucid main"
    # if ver == '5.0':
    #     apt = "deb http://apt.librato.com/debian/ lenny non-free"

if not apt:
    raise Fail("Can't find a cloudkick package for your platform/version")

Execute("apt-update-cloudkick",
    command = "apt-get update",
    action = "nothing")

Execute("curl http://packages.cloudkick.com/cloudkick.packages.key | apt-key add -",
    not_if = "(apt-key list | grep 'Cloudkick' > /dev/null)")

File(apt_list_path,
    owner = "root",
    group ="root",
    mode = 0644,
    content = apt+"\n",
    notifies = [("run", env.resources["Execute"]["apt-update-cloudkick"], True)])

File("/etc/cloudkick.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("cloudkick/cloudkick.conf.j2"))

Package("cloudkick-agent",
    action = "upgrade")

Service("cloudkick-agent",
    supports_restart = True,
    subscribes = [("restart", env.resources["File"]["/etc/cloudkick.conf"])])

Package("libssl0.9.8") # This seems to not get installed for some reason
