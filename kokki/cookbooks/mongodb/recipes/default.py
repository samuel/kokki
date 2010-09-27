
import os
from contextlib import closing
from kokki import *

apt_list_path = '/etc/apt/sources.list.d/mongodb.list'
apt = None
if env.system.platform == "ubuntu":
    ver = env.system.lsb['release']
    if ver == '10.04':
        apt = 'deb http://downloads.mongodb.org/distros/ubuntu 10.4 10gen'
    elif ver == '9.10':
        apt = 'deb http://downloads.mongodb.org/distros/ubuntu 9.10 10gen'
    elif ver == '9.04':
        apt = 'deb http://downloads.mongodb.org/distros/ubuntu 9.4 10gen'
elif env.system.platform == "debian":
    ver = env.system.lsb['release']
    if ver == '5.0':
        apt = 'deb http://downloads.mongodb.org/distros/debian 5.0 10gen'

if not apt:
    raise Fail("Can't find a mongodb package for your platform/version")

Execute("apt-get update", action="nothing")

Execute("apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10",
    not_if = "(apt-key list | grep 10gen.com > /dev/null)")

File(apt_list_path,
    owner = "root",
    group ="root",
    mode = 0644,
    content = apt,
    notifies = [("run", env.resources["Execute"]["apt-get update"], True)])

###

Package("mongodb-stable")

if env.config.mongodb.nodefault:
    Service("mongodb")
    File(env.config.mongodb.configpath,
        action = "delete",
        notifies = [("stop", env.resources["Service"]["mongodb"], True)])
    File("/etc/init/mongodb.conf", action="delete")
    File("/etc/init.d/mongodb", action="delete")
else:
    Directory(env.config.mongodb.dbpath,
        owner = "mongodb",
        group = "mongodb",
        mode = 0755,
        recursive = True)

    Service("mongodb")

    File("/etc/init/mongodb.conf",
        owner = "root",
        group = "root",
        mode = 0644,
        content = Template("mongodb/upstart.conf.j2", variables=dict(mongodb=env.config.mongodb)),
        notifies = [
            ("reload", env.resources["Service"]["mongodb"], True),
        ])

    File(env.config.mongodb.configpath,
        owner = "root",
        group = "root",
        mode = 0644,
        content = Template("mongodb/mongodb.conf.j2", variables=dict(mongodb=env.config.mongodb)),
        notifies = [("restart", env.resources["Service"]["mongodb"])])
