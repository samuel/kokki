
__description__ = "Gearman RPC broker"
__config__ = {
    "gearmand.listen_address": dict(
        description = "IP address to bind to",
        default = "127.0.0.1",
    ),
    "gearmand.user": dict(
        display_name = "Gearmand user",
        description = "User to run the gearmand procses as",
        default = "nobody",
    ),
    "gearmand.pidfile": dict(
        display_name = "Gearmand pid file",
        description = "Path to the PID file for gearmand",
        default = "/var/run/gearmand/gearmand.pid",
    ),
}
