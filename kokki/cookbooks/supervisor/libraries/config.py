
import os
from kokki import *

def configuration(name, content):
    env = Environment.get_instance()
    return File("supervisor-%s" % name,
        content = content,
        owner = "root",
        group = "root",
        mode = 0644,
        path = os.path.join(env.config.supervisor.custom_config_path, name) + ".conf",
        notifies = [("reload", env.resources["Service"]["supervisor"])])
