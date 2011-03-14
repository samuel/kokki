
from kokki import Environment

def Contact(name,
            alias,
            service_notification_commands = "notify-service-by-email",
            host_notification_commands = "notify-host-by-email",
            service_notification_period = "24x7",
            host_notification_period = "24x7",
            service_notification_options = "w,u,c,r",
            host_notification_options = "d,r",
            email = None,
            groups = [],
            **kwargs):
    env = Environment.get_instance()

    for k in ('service_notification_commands',
              'host_notification_commands',
              'service_notification_period',
              'host_notification_period',
              'service_notification_options',
              'host_notification_options'):
        kwargs[k] = locals()[k]

    env.config.nagios3.contacts[name] = kwargs
    for g in groups:
        env.config.nagios3.contactgroups[g].append(name)
