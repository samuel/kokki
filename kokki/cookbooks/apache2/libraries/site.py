
import os
from kokki import *

def site(name, enable=True):
    if enable:
        Execute("a2ensite %s" % name,
            command = "/usr/sbin/a2ensite %s" % name,
            notifies = [("restart", env.resources["Service"]["apache2"])],
            not_if = lambda:os.path.exists("%s/sites-enabled/%s" % (env.config.apache.dir, name)),
            only_if = lambda:os.path.exists("%s/sites-available/%s" % (env.config.apache.dir, name)))
    else:
        Execute("a2dissite %s" % name,
            command = "/usr/sbin/a2dissite %s" % name,
            notifies = [("restart", env.resources["Service"]["apache2"])],
            only_if = lambda:os.path.exists("%s/sites-enabled/%s" % (env.config.apache.dir, name)))
