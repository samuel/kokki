
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
}
