
from kokki import *

env.include_recipe("apache2")

Package("nagios3")
Service("nagios3",
    supports_status = True,
    supports_restart = True,
    supports_reload = True)

##

File("/etc/nagios3/cgi.cfg",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("nagios3/cgi.cfg.j2"),
    notifies = [("restart", env.resources["Service"]["nagios3"])])

if env.system.ec2:
    File("/etc/nagios3/conf.d/host-gateway_nagios3.cfg",
        action = "delete",
        notifies = [("restart", env.resources["Service"]["nagios3"])])

File("/etc/nagios3/conf.d/extinfo_nagios2.cfg",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["nagios3"])])

# nagios3 hostgroups

File("/etc/nagios3/conf.d/hostgroups_nagios2.cfg",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["nagios3"])])

File("nagio3-hostgroups",
    path = "/etc/nagios3/conf.d/hostgroups.cfg",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("nagios3/hostgroups.cfg.j2"),
    notifies = [("restart", env.resources["Service"]["nagios3"])])


# nagios3 contacts

File("/etc/nagios3/conf.d/contacts_nagios2.cfg",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["nagios3"])])

File("nagio3-contacts",
    path = "/etc/nagios3/conf.d/contacts.cfg",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("nagios3/contacts.cfg.j2"),
    notifies = [("restart", env.resources["Service"]["nagios3"])])

env.cookbooks.nagios3.Contact("root",
    alias = "Root",
    service_notification_period = "24x7",
    host_notification_period = "24x7",
    service_notification_options = "w,u,c,r",
    host_notification_options = "d,r",
    service_notification_commands = "notify-service-by-email",
    host_notification_commands = "notify-host-by-email",
    email = "root@localhost")

# nagios3 services

File("/etc/nagios3/conf.d/services_nagios2.cfg",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["nagios3"])])

env.cookbooks.nagios3.Service("HTTP",
    hostgroup_name = "http-servers",
    check_command = "check_http",
    use = "generic-service",
    notification_interval = 0)

env.cookbooks.nagios3.Service("SSH",
    hostgroup_name = "ssh-servers",
    check_command = "check_ssh",
    use = "generic-service",
    notification_interval = 0)

env.cookbooks.nagios3.Service("PING",
    hostgroup_name = "ping-servers",
    check_command = "check_ping!100.0,20%!500.0,60%",
    use = "generic-service",
    notification_interval = 0)

# nagios3 hosts

File("/etc/nagios3/conf.d/localhost_nagios2.cfg",
    action = "delete",
    notifies = [("restart", env.resources["Service"]["nagios3"])])

File("nagios3-hosts"
    path = "/etc/nagios3/conf.d/hosts.cfg",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("nagios3/hosts.cfg.j2"),
    notifies = [("restart", env.resources["Service"]["nagios3"])])

env.cookbooks.nagios3.Host("localhost",
    address = "127.0.0.1",
    groups = ["ssh-servers"])

env.cookbooks.nagios3.Service("Disk Space",
    host_name = "localhost",
    check_command = "check_all_disks!20%!10%")

env.cookbooks.nagios3.Service("Total Processes",
    host_name = "localhost",
    check_command = "check_procs!250!400")

env.cookbooks.nagios3.Service("Current Load",
    host_name = "localhost",
    check_command = "check_load!5.0!4.0!3.0!10.0!6.0!4.0")

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
