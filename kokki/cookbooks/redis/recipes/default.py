
import os
from kokki import *

env.include_recipe("monit")

version = "2.0.3"
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
        "make\n"
        "cp redis-server /usr/local/sbin\n"
        "cp redis-cli redis-benchmark /usr/local/bin\n") % dict(url=url, dirname=dirname, filename=filename))

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
