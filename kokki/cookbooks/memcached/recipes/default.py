
from kokki import *

Package("memcached", action="upgrade")
Package("libmemcache-dev", action="upgrade")
Service("memcached")

File("/etc/memcached.conf",
    content = Template("memcached/memcached.conf.j2"),
    owner = "root",
    group = "root",
    mode = 0644,
    notifies = [("restart", env.resources["Service"]["memcached"], True)])
