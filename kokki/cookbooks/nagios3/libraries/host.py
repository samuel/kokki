
from kokki import Environment

def Host(name,
         alias = None,
         address = None,
         use = "generic-host",
         groups = [],
         action = "create",
         **kwargs):
    env = Environment.get_instance()

    kwargs['name'] = name
    kwargs['alias'] = alias or name
    kwargs['address'] = address or name
    kwargs['use'] = use
    kwargs['services'] = {}
    kwargs['groups'] = groups

    if action == "delete":
        host = env.config.nagios3.hosts.pop(name, None)
        if host:
            for g in host.get('groups', []):
                env.config.nagios3.hostgroups[g]['members'].remove(name)
    else:
        env.config.nagios3.hosts[name] = kwargs
        for g in groups:
            env.config.nagios3.hostgroups[g]['members'].append(name)
