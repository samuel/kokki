
from kokki import *

def Service(service_description, hostgroup_name=None, check_command=None, use="generic-service", notification_interval=0, action="create"):
    env = Environment.get_instance()
    File("/etc/nagios3/conf.d/service_%s.cfg" % service_description.lower(),
        content = Template("nagios3/cfg.j2", dict(
            type = "service",
            values = dict(
                hostgroup_name = hostgroup_name,
                service_description = service_description,
                check_command = check_command,
                use = use,
                notification_interval = 0,
            ).items(),
        )),
        action = action,
        notifies = [("restart", env.resources["Service"]["nagios3"])])
