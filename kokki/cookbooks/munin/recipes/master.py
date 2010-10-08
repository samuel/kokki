
from kokki import *

Package("munin")

File("/etc/munin/munin.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("munin/munin.conf.j2"))
