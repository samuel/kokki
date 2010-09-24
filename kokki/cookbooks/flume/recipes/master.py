
from kokki import *

env.include_recipe("flume")

Package("flume-master")
Service("flume-master",
    supports_restart = True,
    supports_reload = False,
    supports_status = False,
    subscribes = [
        ("restart", env.resources["File"]["flume-config"]),
        ("restart", env.resources["File"]["flume-site-config"]),
        ("restart", env.resources["File"]["flume-log-config"]),
    ])
