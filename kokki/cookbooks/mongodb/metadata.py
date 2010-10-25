
__description__ = "MongoDB database"
__config__ = {
    "mongodb.nodefault": dict(
        description = "Remove the default mongodb.conf and init script",
        default = False,
    ),
    "mongodb.configpath": dict(
        description = "Path to the MongoDB config file",
        default = "/etc/mongodb.conf",
    ),
    "mongodb.options": dict(
        description = "List of command line options (e.g. ['--configsvr'])",
        default = [],
    ),
    "mongodb.dbpath": dict(
        description = "Path where to store the MongoDB database",
        default = "/var/lib/mongodb",
    ),
    "mongodb.logpath": dict(
        description = "Path where to store the MongoDB log",
        default = "/var/log/mongodb",
    ),
    "mongodb.logfilename": dict(
        description = "Name of log file",
        default = "mongodb.log",
    ),
    "mongodb.port": dict(
        description = "Specifies the port number on which Mongo will listen for client connections.",
        default = None,
    ),
    "mongodb.verbose": dict(
        description = "Verbose logging output",
        default = False,
    ),
    "mongodb.rest": dict(
        description = "Allow extended operations at the HTTP Interface",
        default = False,
    ),
    "mongodb.oplog_size": dict(
        description = "Custom size for replication operation log.",
        default = None,
    ),
    "mongodb.op_id_mem": dict(
        description = "Size limit for in-memory storage of op ids.",
        default = None,
    ),
    "mongodb.replica_set": dict(
        description = "<setname>[/<seedlist>] Use replica sets with the specified logical set name.  Typically the optional seed host list need not be specified.",
        default = None,
    ),
    "mongodb.limit_nofile": dict(
        description = "Open file limit set in upstart config",
        default = 32000,
    ),
}
