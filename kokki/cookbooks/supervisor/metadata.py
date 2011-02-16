
__description__ = "Process monitoring"
__config__ = {
    "supervisor.config_path": dict(
        display_name = "Supervisor config path",
        description = "Config file path for supervisor",
        default = "/etc",
    ),
    "supervisor.binary_path": dict(
        display_name = "Supervisor binary path",
        description = "Path to the supervisor binaries",
        default = "/usr/bin", #"/usr/local/bin",
    ),
    "supervisor.pidfile": dict(
        display_name = "Supervisor pid file path",
        description = "Path to the supervisor pid file",
        default = "/var/run/supervisord.pid",
    ),
    "supervisor.logfile": dict(
        display_name = "Supervisor log file path",
        description = "Path to the supervisor log file",
        default = "/var/log/supervisord.log",
    ),
}

# if env.system.platform == "ubuntu":
#     env.supervisor.binary_path = "/usr/local/bin"
# else:
#     env.supervisor.binary_path = "/usr/bin"
