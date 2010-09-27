
__description__ = "Process monitoring"
__config__ = {
    "monit.alert_emails": dict(
        display_name = "Alert emails",
        description = "Emails that should receive alerts about service changes.",
        default = [],
    ),
    "monit.password": dict(
        dispaly_name = "Password",
        description = "Password for accessing web interface",
        default = "m0n1t1tup",
    ),
    'monit.config_path': dict(
        description = "Path to config files",
        default = "/etc/monit",
    ),
}
