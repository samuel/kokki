
from kokki import *

def Host(name,
         alias = None,
         address = None,
         use = "generic-host",
         groups = [],
         action = "create",
         **kwargs):
    env = Environment.get_instance()

    kwargs['alias'] = alias or name
    kwargs['address'] = address or name
    kwargs['use'] = use
    kwargs['services'] = {}

    env.config.nagios3.hosts[name] = kwargs
    for g in groups:
        env.config.nagios3.hostgroups[g]['members'].append(name)

    kwargs['name'] = name

    File("/etc/nagios3/conf.d/host_%s.cfg" % name.lower(),
        content = Template("nagios3/host.cfg.j2", dict(host=kwargs)),
        action = action,
        notifies = [("restart", env.resources["Service"]["nagios3"])])
