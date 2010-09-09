
from os.path import exists
from kokki import *

def site(name, enable=True):
    env = Environment.get_instance()

    if enable:
        cmd = 'nxensite'
    else:
        cmd = 'nxdissite'

    Execute("%s %s" % (cmd,name),
            command = "/usr/sbin/%s %s" % (cmd,name),
            notifies = [("reload", env.resources["Service"]["nginx"])],
            not_if = lambda:exists("%s/sites-enabled/%s" % (env.nginx.dir, name)))
