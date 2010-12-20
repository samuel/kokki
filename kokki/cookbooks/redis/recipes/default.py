
import os
from kokki import *

env.include_recipe("monit")

version = "2.2.0-rc2"
dirname = "redis-%s" % version
filename = "%s.tar.gz" % dirname
url = "http://redis.googlecode.com/files/%s" % filename

Script("install-redis",
    not_if = lambda:os.path.exists("/usr/local/sbin/redis-server"),
    cwd = "/usr/local/src",
    code = (
        "wget %(url)s\n"
        "tar -zxvf %(filename)s\n"
        "cd %(dirname)s\n"
        "make install\n") % dict(url=url, dirname=dirname, filename=filename))

Directory(env.config.redis.dbdir,
    owner = "root",
    group = "root",
    mode = 0700,
    recursive = True)

File("redis.conf",
    path = env.config.redis.configfile,
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("redis/redis.conf.j2"))
env.cookbooks.monit.rc("redis",
    content = Template("redis/monit.conf.j2"))

if "munin.node" in env.included_recipes:
    Package("redis",
        provider = "kokki.providers.package.easy_install.EasyInstallProvider")
    for n in ('active_connections', 'commands', 'connects', 'used_memory'):
        Link("/etc/munin/plugins/redis_%s" % n,
            to = "/etc/munin/python-munin/plugins/redis_%s" % n,
            notifies = [("restart", env.resources['Service']['munin-node'])])
