
from kokki import *

Package("exim4", action="upgrade")
Service("exim4",
    supports_restart=True)

File("/etc/exim4/update-exim4.conf.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("exim4/update-exim4.conf.conf.j2"),
    notifies = [("restart", env.resources["Service"]["exim4"])])
