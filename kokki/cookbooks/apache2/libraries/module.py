
import os
from kokki import Environment, Execute

def module(name, enable=True, conf=False):
    env = Environment.get_instance()

    if conf:
        env.cookbooks.apache2.config(name)

    if enable:
        Execute("a2enmod %s" % name,
            command = "/usr/sbin/a2enmod %s" % name,
            notifies = [("restart", env.resources["Service"]["apache2"])],
            not_if = lambda:os.path.exists("%s/mods-enabled/%s.load" % (env.config.apache.dir, name)))
    else:
        Execute("a2dismod %s" % name,
            command = "/usr/sbin/a2dismod %s" % name,
            notifies = [("restart", env.resources["Service"]["apache2"])],
            only_if = lambda:os.path.exists("%s/mods-enabled/%s.load" % (env.config.apache.dir, name)))
