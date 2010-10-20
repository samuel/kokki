
from kokki import *

env.include_recipe("flume")

Package("flume-node")

import os
def flume_node_status():
    pid_path = "/var/run/flume/flume-flume-node.pid"
    try:
        with open(pid_path, "rb") as fp:
            pid = int(fp.read().strip())
        os.getpgid(pid) # Throws OSError if processes doesn't exist
    except (IOError, OSError, ValueError):
        return False
    return True

Service("flume-node",
    supports_restart = True,
    supports_reload = False,
    status_command = flume_node_status,    
    subscribes = [
        ("restart", env.resources["File"]["flume-config"]),
        ("restart", env.resources["File"]["flume-site-config"]),
        ("restart", env.resources["File"]["flume-log-config"]),
        ("restart", env.resources["File"]["flume-daemon-sh"]),
    ])
