
from kokki import Package, Execute, File, Fail

Package("erlang")

apt_list_path = '/etc/apt/sources.list.d/rabbitmq.list'
apt = None
if env.system.platform in ("ubuntu", "debian"):
    apt = "deb http://www.rabbitmq.com/debian/ testing main"

if not apt:
    raise Fail("Can't find a rabbitmq package for your platform/version")

Execute("apt-update-rabbitmq",
    command = "apt-get update",
    action = "nothing")

Execute("curl http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | apt-key add -",
    not_if = "(apt-key list | grep rabbitmq > /dev/null)")

File(apt_list_path,
    owner = "root",
    group ="root",
    mode = 0644,
    content = apt+"\n",
    notifies = [("run", env.resources["Execute"]["apt-update-rabbitmq"], True)])

Package("rabbitmq-server")
