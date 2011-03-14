
__description__ = "PostgreSQL server and clients"
__config__ = {
    "postgresql84.data_dir": dict(
        display_name = "PostgreSQL Data Directory",
        description = "Location of the PostgreSQL databases",
        default = "/var/lib/postgresql/8.4/main",
    ),
    "postgresql84.config_dir": dict(
        display_name = "PostgreSQL Config Directory",
        description = "Location of the PostgreSQL configuration files",
        default = "/etc/postgresql/8.4/main",
    ),
    "postgresql84.pidfile": dict(
        display_name = "PostgreSQL PID File",
        description = "Path to the PostgreSQL pid file",
        default = "/var/run/postgresql/8.4-main.pid",
    ),
    "postgresql84.listen_addresses": dict(
        display_name = "PostgreSQL listen addresses",
        description = "IP addresses PostgreSQL should listen on (* for all interfaces)",
        default = "[localhost]",
    ),
    "postgresql84.port": dict(
        display_name = "PostgreSQL port",
        description = "Port PostgreSQL should bind to",
        default = 5432,
    ),
    "postgresql84.max_connections": dict(
        display_name = "PostgreSQL max connections",
        description = "Maximum numbers of connections",
        default = 100,
    ),
    "postgresql84.auth": dict(
        display_name = "PostgreSQL authentication",
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
    "postgresql84.log_min_duration_statement": dict(
        display_name = "PostgreSQL Logging Minimum Statement Duration",
        description = "-1 is disabled, 0 logs all statements and their durations, > 0 logs only statements running at least this number of milliseconds",
        default = -1,
    ),
    "postgresql84.skytools.ticker.job_name": dict(
        display_name = "Skytools ticker job name",
        description = "Name used for logging and other such things",
        default = "Ticker1",
    ),
    "postgresql84.skytools.ticker.db": dict(
        display_name = "Skytools ticker database DSN",
        description = "PostgreSQL connection string (dbname, user, password, host, port)",
        default = "dbname=P",
    ),
    "postgresql84.skytools.ticker.logfile": dict(
        display_name = "Skytools ticker log file path",
        description = "Path to the log file. Can include %(job_name)s",
        default = "/var/log/%(job_name)s.log",
    ),
    "postgresql84.skytools.ticker.pidfile": dict(
        display_name = "Skytools ticker pid file path",
        description = "Path to the pid file. Can include %(job_name)s",
        default = "/var/run/%(job_name)s.pid",
    ),
    "postgresql84.skytools.londiste.job_name": dict(
        display_name = "Skytools londiste job name",
        description = "Name used for logging and other such things",
        default = "Londiste1",
    ),
    "postgresql84.skytools.londiste.provider_db": dict(
        display_name = "Skytools londiste provider database DSN",
        description = "PostgreSQL connection string (dbname, user, password, host, port)",
        default = "dbname=P host=127.0.0.1",
    ),
    "postgresql84.skytools.londiste.subscriber_db": dict(
        display_name = "Skytools londiste subscriber database DSN",
        description = "PostgreSQL connection string (dbname, user, password, host, port)",
        default = "dbname=S host=127.0.0.1",
    ),
    "postgresql84.skytools.londiste.pgq_queue_name": dict(
        display_name = "Skytools londiste PGQ queue name",
        description = "PQG queue name for londiste (it will be used as sql ident so no dots/spaces).",
        default = "londiste_replica",
    ),
    "postgresql84.skytools.londiste.logfile": dict(
        display_name = "Skytools londiste log file path",
        description = "Path to the log file. Can include %(job_name)s",
        default = "/var/log/%(job_name)s.log ",
    ),
    "postgresql84.skytools.londiste.pidfile": dict(
        display_name = "Skytools londiste pid file path",
        description = "Path to the pid file. Can include %(job_name)s",
        default = "/var/run/%(job_name)s.pid ",
    ),
    'postgresql84.locale': dict(
        description = "Locale",
        default = None,
    ),
}
def __loader__(kit):
    if kit.config.postgresql84.locale is None:
        postgresql_locale = kit.system.locales[0]
        for l in kit.system.locales:
            if 'utf8' in l.lower() or 'utf-8' in l.lower():
                postgresql_locale = l
                break
        kit.config.postgresql84.locale = postgresql_locale
