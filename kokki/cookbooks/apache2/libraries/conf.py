
from kokki import Environment, File, Template

def config(name):
    env = Environment.get_instance()

    File("%s/mods-available/%s.conf" % (env.config.apache.dir, name),
        content = Template('apache2/mods/%s.conf.j2' % name),
        notifies = [("restart", env.resources["Service"]["apache2"])])
