
__description__ = "Process monitoring"
__config__ = {
    "supervisor.config_path": dict(
        description = "Config file path for supervisor",
        default = "/etc/supervisor/supervisord.conf",
    ),
    "supervisor.socket_path": dict(
        description = "Unix socket path",
        default = "/var/run/supervisor.sock",
    ),
    "supervisor.custom_config_path": dict(
        description = "Path to custom supervisor config files",
        default = "/etc/supervisor/conf.d", 
    ),
    "supervisor.binary_path": dict(
        description = "Path to the supervisor binaries",
        default = "/usr/bin",
    ),
    "supervisor.pidfile": dict(
        description = "Path to the supervisor pid file",
        default = "/var/run/supervisord.pid",
    ),
    "supervisor.logfile": dict(
        description = "Path to the supervisor log file",
        default = "/var/log/supervisord.log",
    ),
}

# if env.system.platform == "ubuntu":
#     env.supervisor.binary_path = "/usr/local/bin"
# else:
#     env.supervisor.binary_path = "/usr/bin"
