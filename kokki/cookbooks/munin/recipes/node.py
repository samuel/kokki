
from kokki import Package, File, Template, Service

if env.system.platform == "amazon":
    Package("perl-NetAddr-IP")

Package("munin-node")

File("munin-node.conf",
    path = "/etc/munin/munin-node.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("munin/munin-node.conf.j2"))

Service("munin-node",
    subscribes = [("restart", env.resources["File"]["munin-node.conf"])])

File("/etc/munin/plugin-conf.d/python",
    owner = "root",
    group = "root",
    mode = 0644,
    content = (
        "[*]\n"
        "env.PYTHON_EGG_CACHE /tmp/munin-egg-cache\n"
    ),
    notifies = [("restart", env.resources["Service"]["munin-node"])])

if env.system.ec2:
    File("/etc/munin/plugins/if_err_eth0",
        action = "delete",
        notifies = [("restart", env.resources["Service"]["munin-node"])])
