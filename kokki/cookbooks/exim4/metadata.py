
__description__ = "Exim4 mail server"
__config__ = {
    "exim4.configtype": dict(
        description = "Type of config for mail sending (e.g. satellite)",
        default = "satellite",
    ),
    "exim4.other_hostnames": dict(
        description = "Other host names to receive mail for",
        default = "localhost",
    ),
    "exim4.local_interfaces": dict(
        description = "Local interfaces to bind to",
        default = "127.0.0.1",
    ),
    "exim4.readhost": dict(
        description = "Read host",
        default = "localhost",
    ),
    "exim4.smarthost": dict(
        description = "Host through which to forward mail",
        default = "",
    ),
    "exim4.auth": dict(
        description = "Credentials to use when authenticating to a remote server. List of dictionaries with keys 'domain', 'login', and 'password'.",
        default = [],
    ),
}
