
__description__ = "MongoDB database"
__config__ = {
    "mongodb.dbpath": dict(
        description = "Path where to store the MongoDB database",
        default = "/var/lib/mongodb",
    ),
    "mongodb.logpath": dict(
        description = "Path where to store the MongoDB log",
        default = "/var/log/mongodb/mongodb.log",
    ),
}
