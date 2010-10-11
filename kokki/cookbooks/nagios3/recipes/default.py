
from kokki import *

env.include_recipe("apache2")

Package("nagios3")
Service("nagios3",
    supports_status = True,
    supports_restart = True,
    supports_reload = True,
    action = "start")

##

File("/etc/nagios3/cgi.cfg",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("nagios3/cgi.cfg.j2"),
    notifies = [("restart", env.resources["Service"]["nagios3"])])

File("/etc/nagios3/conf.d/contacts_nagios2.cfg",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["nagios3"])])

File("/etc/nagios3/conf.d/contacts.cfg",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("nagios3/contacts.cfg.j2"),
    notifies = [("restart", env.resources["Service"]["nagios3"])])

if env.system.ec2:
    File("/etc/nagios3/conf.d/host-gateway_nagios3.cfg",
        action = "delete",
        notifies = [("restart", env.resources["Service"]["nagios3"])])

##

File("/etc/apache2/conf.d/nagios3.conf",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["apache2"])])

File("/etc/apache2/sites-available/nagios3",
    owner = "www-data",
    group = "www-data",
    mode = 0644,
    content = Template("nagios3/apache2-site.j2"),
    notifies = [("restart", env.resources["Service"]["apache2"])])

env.cookbooks.apache2.site("nagios3")
