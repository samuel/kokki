
__config__ = {
    "mysql.server_root_password": dict(
        default = "changeme",
    ),
    "mysql.datadir": dict(
        description = "Location of MySQL database",
        default = "/var/lib/mysql",
    ),
    "mysql.bind_address": dict(
        description = "Address that MySQLd should listen on",
        default = "127.0.0.1",
    ),
    "mysql.tunable.key_buffer": dict(
        default = "250M",
    ),
    "mysql.tunable.max_connections": dict(
        default = 800,
    ),
    "mysql.tunable.wait_timeout": dict(
        default = 180,
    ),
    "mysql.tunable.net_read_timeout": dict(
        default = 30,
    ),
    "mysql.tunable.net_write_timeout": dict(
        default = 30,
    ),
    "mysql.tunable.back_log": dict(
        default = 128,
    ),
    "mysql.tunable.table_cache": dict(
        default = 128,
    ),
    "mysql.tunable.max_heap_table_size": dict(
        default = "32M",
    ),
}
