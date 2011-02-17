
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

    File(config.configpath,
        owner = "root",
        group = "root",
        mode = 0644,
        content = Template("mongodb/mongodb.conf.j2", variables=dict(mongodb=config)))
        # notifies = [("restart", env.resources["MonitService"]["mongodb-%s" % name])])

    controller = kwargs.get("controller")
    if controller == "monit":
        env.include_recipe("monit")
        env.cookbooks.monit.rc("mongodb-%s" % name,
            Template("mongodb/monit.conf.j2", variables=dict(name=name, mongodb=config)))
        env.cookbooks.monit.MonitService("mongodb-%s" % name,
            subscribes = [("restart", env.resources["File"][config.configpath])])
    elif controller == "supervisord":
        env.include_recipe("supervisor")
        env.cookbooks.supervisor.configuration("mongodb-%s" % name,
            Template("mongodb/supervisord.conf.j2", variables=dict(name=name, mongodb=config)))
        env.cookbooks.supervisor.SupervisorService("mongodb-%s" % name,
            subscribes = [("restart", env.resources["File"][config.configpath])])
    else:
        Service("mongodb-%s" % name,
             subscribes = [("restart", env.resources["File"][config.configpath])])
        File("/etc/init/mongodb-%s.conf" % name,
            owner = "root",
            group = "root",
            mode = 0644,
            content = Template("mongodb/upstart.conf.j2", variables=dict(mongodb=config)),
            notifies = [
                ("reload", env.resources["Service"]["mongodb-%s" % name], True),
            ])
