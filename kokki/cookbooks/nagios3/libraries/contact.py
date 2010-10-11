

from kokki import *

def Contact(name,
            alias,
            service_notification_commands = "notify-service-by-email",
            host_notification_commands = "notify-host-by-email",
            service_notification_period = "24x7",
            host_notification_period = "24x7",
            service_notification_options = "w,u,c,r",
            host_notification_options = "d,r",
            email = None,
            **kwargs):
    env = Environment.get_instance()

    kwargs['contact_name'] = name
    for k in ('service_notification_commands',
              'host_notification_commands',
              'service_notification_period',
              'host_notification_period',
              'service_notification_options',
              'host_notification_options'):
        kwargs[k] = locals()[k]

    env.config.nagios3.contacts[name] = kwargs
    # env.delayed_actions

    # kwargs['contact_name'] = name
    # for k in ('service_notification_commands',
    #           'host_notification_commands',
    #           'service_notification_period',
    #           'host_notification_period',
    #           'service_notification_options',
    #           'host_notification_options'):
    #     kwargs[k] = locals()[k]
    # File("/etc/nagios3/conf.d/contact_%s.cfg" % name.lower(),
    #     content = Template("nagios3/cfg.j2", dict(
    #         type = "contact",
    #         values = kwargs.items(),
    #     )),
    #     action = action,
    #     notifies = [("restart", env.resources["Service"]["nagios3"])])
