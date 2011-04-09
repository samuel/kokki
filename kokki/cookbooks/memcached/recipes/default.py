
from kokki import Package, Service, File, Template, Link

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
            "export SL_NAME=memcached\n"
        ),
        notifies = [("restart", env.resources["Service"]["memcached"])])

if "munin.node" in env.included_recipes:
    for n in ('bytes', 'connections', 'curr_items', 'items', 'queries'):
        Link("/etc/munin/plugins/memcached_%s" % n,
            to = "/etc/munin/python-munin/plugins/memcached_%s" % n,
            notifies = [("restart", env.resources['Service']['munin-node'])])
