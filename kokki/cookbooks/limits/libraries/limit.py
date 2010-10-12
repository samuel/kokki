
from kokki import *

def Limit(domain, type, item, value, action="include"):
    env = Environment().get_instance()

    for i, l in enumerate(env.config.limits):
        if l['domain'] == domain and l['type'] == type and l['item'] == item:
            del env.config.limits[i]
            break

    if action == "include":
        env.config.limits.append(dict(domain=domain, type=type, item=item, value=value))
