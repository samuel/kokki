
from kokki import *

def config(name, content):
    env = Environment.get_instance()
    return File("supervisor-%s" % name,
        content = content,
        owner = "root",
        group = "root",
        mode = 0644,
        path = "%s/supervisor.d/%s" % (env.config.supervisor.config_path, name)),
        notifies = [("reload", env.resources["Service"]["supervisor"])])
