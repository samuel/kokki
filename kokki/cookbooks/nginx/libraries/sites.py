
from os.path import exists
from kokki import *

def site(name, enable=True):
    env = Environment.get_instance()

    if enable:
        cmd = 'nxensite'
    else:
        cmd = 'nxdissite'

    def _not_if():
        e = exists("%s/sites-enabled/%s" % (env.config.nginx.dir, name))
        return e if enable else not e

    Execute("%s %s" % (cmd, name),
            command = "/usr/sbin/%s %s" % (cmd, name),
            notifies = [("reload", env.resources["Service"]["nginx"])],
            not_if = _not_if)
