
from kokki import *

Package("munin")
Service("munin",
    supports_status = True,
    supports_restart = True)

File("/etc/munin/munin.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("munin/munin.conf.j2"),
    notifies = [("restart", env.resources["Service"]["munin"])])
