
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

if "librato.silverline" in env.included_recipes:
    File("/etc/default/memcached",
        owner = "root",
        group = "root",
        mode = 0644,
        content = (
            "ENABLE_MEMCACHED=yes\n"
            "export LM_CONTAINER_NAME=nginx\n"
            "export LM_TAG_NAMES=nginx:webserver\n"
        ),
        notifies = [("restart", env.resources["Service"]["memcached"])])

if "munin.node" in env.included_recipes:
    for n in ('bytes', 'connections', 'curr_items', 'items', 'queries'):
        Link("/etc/munin/plugins/memcached_%s" % n,
            to = "/etc/munin/python-munin/plugins/memcached_%s" % n,
            notifies = [("restart", env.resources['Service']['munin-node'])])
