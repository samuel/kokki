
__config__ = {
    "mysql.server_root_password": dict(
        default = "changeme",
    ),
    "mysql.server_repl_password": dict(
        default = None,
    ),
    "mysql.server_debian_password": dict(
        default = "changeme",
    ),
    "mysql.grants": dict(
        default = [
            # dict(user, host, database, password, permissions)
        ],
    ),
    "mysql.datadir": dict(
        description = "Location of MySQL database",
        default = "/var/lib/mysql",
    ),
    "mysql.bind_address": dict(
        description = "Address that MySQLd should listen on",
        default = "127.0.0.1",
    ),
    "mysql.ft_min_word_len": dict(
        description = "Minimum word length for items in the full-text index",
        default = None,
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
    "mysql.tunable.thread_stack": dict(
        default = "128K"
    ),
    # Replication
    "mysql.server_id": dict(
        default = None,
    ),
    "mysql.log_bin": dict(
        default = None, # /var/log/mysql/mysql-bin.log
    ),
    "mysql.expire_logs_days": dict(
        default = 10,
    ),
    "mysql.max_binlog_size": dict(
        default = "100M",
    ),
}