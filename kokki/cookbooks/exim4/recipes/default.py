
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

File("/etc/exim4/exim4.conf.localmacros",
    owner = "root",
    group = "root",
    mode = 0644,
    content = "AUTH_CLIENT_ALLOW_NOTLS_PASSWORDS = 1\n",
    notifies = [("restart", env.resources["Service"]["exim4"])])

File("/etc/exim4/passwd.client",
    mode = 0600,
    content = Template("exim4/passwd.client.j2"),
    notifies = [("restart", env.resources["Service"]["exim4"])])
