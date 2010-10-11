
__description__ = "Server monitoring"
__config__ = {
    "nagios3.contacts": dict(
        description = "Dictionary of contacts with name as key and value as a dictionary with additional options",
        default = {
            # "root": dict(
            #     alias = "Root",
            #     service_notification_period = "24x7",
            #     host_notification_period = "24x7",
            #     service_notification_options = "w,u,c,r",
            #     host_notification_options = "d,r",
            #     service_notification_commands = "notify-service-by-email",
            #     host_notification_commands = "notify-host-by-email",
            #     email = "root@localhost",
            # ),
        },
    ),
    "nagios3.hosts": dict(
        description = "Dictionary of hosts with name as key and value as dictionary with keys use, alias, and address",
        default = {},
    ),
    "nagios3.contactgroups": dict(
        description = "Dictionary of contact groups with name as key and value as a dictionary with alias and members:list",
        default = {
            "admins": dict(
                alias = "Nagios Administrators",
                members = [],
            ),
        },
    ),
    "nagios3.hostgroups": dict(
        description = "Dictionary of host groups with name as key and value as a dictionary with alias and members",
        default = {
            # A simple wildcard hostgroup
            "all": dict(
                alias = "All Servers",
                members = ["*"],
            ),
            # A list of your web servers
            "http-servers": dict(
                alias = "HTTP Servers",
                members = [],
            ),
            # A list of your ssh-accessible servers
            "ssh-servers": dict(
                alias = "SSH Servers",
                members = [],
            ),
            # nagios doesn't like monitoring hosts without services, so this is
            # a group for devices that have no other "services" monitorable
            # (like routers w/out snmp for example)
            "ping-servers": dict(
                alias = "Pingable Servers",
                members = [],
            ),
        },
    ),
    # cgi
    "nagios3.default_user_name": dict(
        description =
            "Setting this variable will define a default user name that can "
            "access pages without authentication.  This allows people within a "
            "secure domain (i.e., behind a firewall) to see the current status "
            "without authenticating.  You may want to use this to avoid basic "
            "authentication if you are not using a secure server since basic "
            "authentication transmits passwords in the clear.\n"
            "Important:  Do not define a default username unless you are "
            "running a secure web server and are sure that everyone who has "
            "access to the CGIs has been authenticated in some manner!  If you "
            "define this variable, anyone who has not authenticated to the web "
            "server will inherit all rights you assign to this user!",
        default = None,
    ),
    "nagios3.default_admin": dict(
        description = "Default username that has full access",
        default = "nagiosadmin",
    ),
    "nagios3.authorized_for_system_information": dict(
        description = 
            "SYSTEM/PROCESS INFORMATION ACCESS\n"
            "This option is a comma-delimited list of all usernames that "
            "have access to viewing the Nagios process information as "
            "provided by the Extended Information CGI (extinfo.cgi). By "
            "default, *no one* has access to this unless you choose to "
            "not use authorization.  You may use an asterisk (*) to "
            "authorize any user who has authenticated to the web server.",
        default = None,
    ),
    "nagios3.authorized_for_configuration_information": dict(
        description =
            "CONFIGURATION INFORMATION ACCESS\n"
            "This option is a comma-delimited list of all usernames that "
            "can view ALL configuration information (hosts, commands, etc). "
            "By default, users can only view configuration information "
            "for the hosts and services they are contacts for. You may use "
            "an asterisk (*) to authorize any user who has authenticated "
            "to the web server.",
        default = None,
    ),
    "nagios3.authorized_for_system_commands": dict(
        description =
            "SYSTEM/PROCESS COMMAND ACCESS\n"
            "This option is a comma-delimited list of all usernames that "
            "can issue shutdown and restart commands to Nagios via the "
            "command CGI (cmd.cgi).  Users in this list can also change "
            "the program mode to active or standby. By default, *no one* "
            "has access to this unless you choose to not use authorization. "
            "You may use an asterisk (*) to authorize any user who has "
            "authenticated to the web server.",
        default = None,
    ),
    "nagios3.authorized_for_all_services": dict(
        description =
            "GLOBAL HOST/SERVICE VIEW ACCESS\n"
            "These two options are comma-delimited lists of all usernames that "
            "can view information for all hosts and services that are being "
            "monitored.  By default, users can only view information "
            "for hosts or services that they are contacts for (unless you "
            "you choose to not use authorization). You may use an asterisk (*) "
            "to authorize any user who has authenticated to the web server.",
        default = None,
    ),
    "nagios3.authorized_for_all_hosts": dict(
        description = "See authorized_for_all_services",
        default = None,
    ),
    "nagios3.authorized_for_all_service_commands": dict(
        description =
            "GLOBAL HOST/SERVICE COMMAND ACCESS\n"
            "These two options are comma-delimited lists of all usernames that "
            "can issue host or service related commands via the command "
            "CGI (cmd.cgi) for all hosts and services that are being monitored. "
            "By default, users can only issue commands for hosts or services "
            "that they are contacts for (unless you you choose to not use "
            "authorization).  You may use an asterisk (*) to authorize any "
            "user who has authenticated to the web server.",
        default = None,
    ),
    "nagios3.authorized_for_all_host_commands": dict(
        description = "See authorized_for_all_service_commands",
        default = None,
    ),
}
