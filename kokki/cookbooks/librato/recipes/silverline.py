
from kokki import *

env.include_recipe("librato")

Package("librato-silverline")

Service("silverline", action="start")

Execute("reload-silverline",
    command = "killall lmd",
    action = "nothing")

File("/etc/load_manager/lmd.conf",
    owner = "root",
    group = "root",
    mode = 0600,
    content = Template("librato/lmd.conf.j2"),
    notifies = [("run", env.resources["Execute"]["reload-silverline"])])

File("/etc/load_manager/lmc.conf",
    owner = "root",
    group = "root",
    mode = 0600,
    content = Template("librato/lmc.conf.j2"))
