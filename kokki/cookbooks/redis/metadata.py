
__description__ = "Redis in-memory database"
__config__ = {
    "redis.configfile": dict(
        description = "Path to the config file",
        default = "/etc/redis.conf",
    ),
    "redis.bind": dict(
        description = "Interface to listen on",
        default = "127.0.0.1",
    ),
    "redis.port": dict(
        description = "Accept connections on the specified port",
        default = 6379,
    ),
    "redis.timeout": dict(
        description = "Close the connection after a client is idle for N seconds (0 to disable)",
        default = 300,
    ),
    "redis.pidfile": dict(
        description = "The file which to write the pid to.",
        default = "/var/run/redis.pid",
    ),
    "redis.dbdir": dict(
        description = "For default save/load DB in/from the working directory",
        default = "/var/db/redis/",
    ),
    "redis.appendonly": dict(
        description = "Use the append only file for persistence",
        default = True,
    ),
    "redis.appendfsync": dict(
        description = "How often to fsync the AOF file (no, everysec, always)",
        default = "everysec",
    ),
    "redis.databases": dict(
        description = "Set the number of databases.",
        default = 16,
    ),
    "redis.logfile": dict(
        description = "File for Redis's log",
        default = "/var/log/redis.log",
    ),
    "redis.loglevel": dict(
        description = "How much Redis should log",
        default = "notice",
    ),
    "redis.master.ip": dict(
        description = "This instance of redis is a slave of a master at the given IP",
        default = None,
    ),
    "redis.master.port": dict(
        description = "Port number for the master server. If slaveof.ip is specified but thit is not then defalts to redis.port.",
        default = None,
    ),
    "redis.maxmemory": dict(
        description = "Don't use more memory than the specified amount of bytes.",
        default = None,
    ),
}
