
__description__ = "PostgreSQL database 9.0.0"
__config__ = {
    "postgresql9.root_dir": dict(
        default = "/usr/local/pgsql",
    ),
    "postgresql9.data_dir": dict(
        description = "Location of the PostgreSQL databases",
        default = "{config[postgresql9.root_dir][default]}/data/main",
    ),
    "postgresql9.config_dir": dict(
        description = "Location of the PostgreSQL configuration files",
        default = "{config[postgresql9.root_dir][default]}/config",
    ),
    "postgresql9.pidfile": dict(
        description = "Path to the PostgreSQL pid file",
        default = "{config[postgresql9.root_dir][default]}/pid",
    ),
    "postgresql9.unix_socket_directory": dict(
        default = "{config[postgresql9.root_dir][default]}",
    ),
    "postgresql9.listen_addresses": dict(
        description = "IP addresses PostgreSQL should listen on (* for all interfaces)",
        default = ["localhost"],
    ),
    "postgresql9.port": dict(
        description = "Port PostgreSQL should bind to",
        default = 5432,
    ),
    "postgresql9.max_connections": dict(
        description = "Maximum numbers of connections",
        default = 100,
    ),
    "postgresql9.auth": dict(
        description = "List of auth configs",
        default = [
            dict(
                type = "local",
                database = "all",
                user = "all",
                method = "ident",
            ),
            dict(
                type = "host",
                database = "all",
                user = "all",
                cidr = "127.0.0.1/32",
                method = "md5",
            ),
            dict(
                type = "host",
                database = "all",
                user = "all",
                cidr = "::1/128",
                method = "md5",
            ),
        ],
    ),
    "postgresql9.ssl": dict(
        default = False,
    ),
    "postgresql9.shared_buffers": dict(
        default = "32MB",
    ),
    "postgresql9.log_min_duration_statement": dict(
        description = "-1 is disabled, 0 logs all statements and their durations, > 0 logs only statements running at least this number of milliseconds",
        default = -1,
    ),
    # Streaming replication
    "postgresql9.max_wal_sender": dict(
        description = "Maximum number of WAL sender processes",
        default = 0,
    ),
    "postgresql9.wal_sender_delay": dict(
        description = "walsender cycle time, 1-10000 milliseconds",
        default = "200ms",
    ),
    # Standby Servers
    "postgresql9.hot_standby": dict(
        description = "Allow queries during discovery",
        default = False,
    ),
    # Install options
    "postgresql9.package_url": dict(
        default = "http://wwwmaster.postgresql.org/redir/198/h/source/v9.0.0/postgresql-9.0.0.tar.gz",
    ),
    "postgresql9.with_perl": dict(
        default = True,
    ),
    "postgresql9.with_python": dict(
        default = True,
    ),
    "postgresql9.with_xml": dict(
        default = True,
    ),
    "postgresql9.with_openssl": dict(
        default = True,
    ),
}

for k, v in __config__.iteritems():
    if isinstance(v['default'], basestring):
        v["default"] = v["default"].format(config=__config__)
