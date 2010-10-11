
from kokki import *

def Service(service_description, host_name=None, hostgroup_name=None, check_command=None, use="generic-service", notification_interval=0, action="create"):
    env = Environment.get_instance()

    values = dict(
        host_name = host_name,
        hostgroup_name = hostgroup_name,
        service_description = service_description,
        check_command = check_command,
        use = use,
        notification_interval = notification_interval,
    )

    if host_name:
        env.config.nagios3.hosts[host_name]["services"][service_description] = values
        return

    File("/etc/nagios3/conf.d/service_%s.cfg" % service_description.lower(),
        content = Template("nagios3/service.cfg.j2", values),
        action = action,
        notifies = [("restart", env.resources["Service"]["nagios3"])])
