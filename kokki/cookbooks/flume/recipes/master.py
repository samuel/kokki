
from kokki import *

env.include_recipe("flume")

Package("flume-master")
Service("flume-master",
    subscribes = [
        ("restart", env.resources["File"]["flume-config"]),
        ("restart", env.resources["File"]["flume-site-config"]),
        ("restart", env.resources["File"]["flume-log-config"]),
    ])
