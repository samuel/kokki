
import os
from kokki import *

def setup(name, **kwargs):
    env = Environment.get_instance()
    config = env.config.mongodb.copy()
    config.update(kwargs)

    config['configpath'] = "/etc/mongodb/%s.conf" % name
    if 'dbpath' not in kwargs:
        config['dbpath'] = os.path.join(config.dbpath, name)
    if 'logfilename' not in kwargs:
        config['logfilename'] = "%s.log" % name

    Directory("/etc/mongodb",
        owner = "root",
        group = "root",
        mode = 0755)

    Directory(config.dbpath,
        owner = "mongodb",
        group = "mongodb",
        mode = 0755,
        recursive = True)

    Service("mongodb-%s" % name)

    File("/etc/init/mongodb-%s.conf" % name,
        owner = "root",
        group = "root",
        mode = 0644,
        content = Template("mongodb/upstart.conf.j2", variables=dict(mongodb=config)),
        notifies = [
            ("reload", env.resources["Service"]["mongodb-%s" % name], True),
        ])

    File(config.configpath,
        owner = "root",
        group = "root",
        mode = 0644,
        content = Template("mongodb/mongodb.conf.j2", variables=dict(mongodb=config)),
        notifies = [("restart", env.resources["Service"]["mongodb-%s" % name])])
