
from kokki import Environment, File

def rc(name, content):
    env = Environment.get_instance()
    return File("monitrc-%s" % name,
        content = content,
        owner = "root",
        group = "root",
        mode = 0644,
        path = "%s/monit.d/%s" % (env.config.monit.config_path, name),
        notifies = [("restart", env.resources["Service"]["monit"])])
