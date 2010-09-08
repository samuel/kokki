
from kokki import *

Package("munin-node")

File("munin-node.conf",
    path = "/etc/munin/munin-node.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("munin/munin-node.conf.j2"))

Service("munin-node",
    subscribes = [("restart", env.resources["File"]["munin-node.conf"])])
