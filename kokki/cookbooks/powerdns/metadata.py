
__description__ = "PowerDNS server and recursor"
__config__ = {
    "powerdns.backends": dict(
        description = "List of backend modules to install",
        default = ["pipe"],
    ),
    "powerdns.pipe_command": dict(
        description = "Pipe command",
        default = None,
    ),
    "powerdns.allow_recursion": dict(
        description = "List of addresses from which to allow recursion",
        default = "127.0.0.1",
    ),
    "powerdns.recursor": dict(
        description = "IP address of recursing nameserver if desired",
        default = None,
    ),
}
