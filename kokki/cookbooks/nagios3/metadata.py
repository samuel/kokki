
__description__ = "Server monitoring"
__config__ = {
    "nagios3.contacts": dict(
        description = "Dictionary of contacts with name as key and value as a dictionary with additional options",
        default = {
            "root": dict(
                alias = "Root",
                service_notification_period = "24x7",
                host_notification_period = "24x7",
                service_notification_options = "w,u,c,r",
                host_notification_options = "d,r",
                service_notification_commands = "notify-service-by-email",
                host_notification_commands = "notify-host-by-email",
                email = "root@localhost",
            ),
        },
    ),
    "nagios3.contactgroups": dict(
        description = "Dictionary of contact groups with name as key and value as a dictionary with alias and members:list",
        default = {
            "admins": dict(
                alias = "Nagios Administrators",
                members = ["root"],
            ),
        },
    ),
}
