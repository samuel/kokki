
from kokki import *

env.include_recipe("flume")

Package("flume-node")
Service("flume-node",
    subscribes = [
        ("restart", env.resources["File"]["flume-config"]),
        ("restart", env.resources["File"]["flume-site-config"]),
        ("restart", env.resources["File"]["flume-log-config"]),
    ])
