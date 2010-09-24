
from kokki import *

env.include_recipe("flume")

Package("flume-node")
Service("flume-node",
    supports_restart = True,
    supports_reload = False,
    supports_status = False,
    subscribes = [
        ("restart", env.resources["File"]["flume-config"]),
        ("restart", env.resources["File"]["flume-site-config"]),
        ("restart", env.resources["File"]["flume-log-config"]),
    ])
