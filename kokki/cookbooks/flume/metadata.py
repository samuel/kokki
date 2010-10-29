
__description__ = "Data flows"
__config__ = {
    "flume.master.servers": dict(
        description = "A comma-separated list of hostnames, one for each machine in the Flume Master.",
        default = None,
    ),
    "flume.plugin.classes": dict(
        description = "Comma separated list of plugin classes",
        default = None,
    ),
    "flume.collector.event.host": dict(
        description = "Host name of the default 'remote' collector",
        default = None,
    ),
    "flume.collector.post": dict(
        description = "Default tcp port that the collector listen to in order to receive events it is collecting",
        default = None,
    ),
    "flume.master.zk.logdir": dict(
        description = "Base directory in which the ZBCS stores data",
        default = "/tmp/flume-zk",
    ),
    "flume.master.zk.server.quorum.port": dict(
        description = "ZooKeeper quorum port",
        default = 3182,
    ),
    "flume.master.zk.server.election.port": dict(
        description = "ZooKeeper election port",
        default = 3183,
    ),
    "flume.master.zk.client.port": dict(
        description = "ZooKeeper client port",
        default = 3181,
    ),
    "flume.master.zk.use.external": dict(
        description = "Use an external ZooKeeper cluter",
        default = False,
    ),
    "flume.master.zk.servers": dict(
        description = "Comma-separated list of external ZooKeeper servers",
        default = None,
    ),
    "flume.agent.logdir": dict(
        description = "This is the directory that write-ahead logging data"
                      "or disk-failover data is collected from applicaitons"
                      "gets written to. The agent watches this directory.",
        default = "/tmp/flume/agent",
    ),
    "flume.collector.dfs.dir": dict(
        description = "This is a dfs directory that is the the final resting"
                      "place for logs to be stored in.  This defaults to a local dir in"
                      "/tmp but can be hadoop URI path that such as hdfs://namenode/path/",
        default = "file:///tmp/flume/collected",
    ),
    "flume.collector.dfs.compress.gzip": dict(
        description = "Writes compressed output in gzip format to dfs.",
        value = False,
    ),
    "flume.log_level": dict(
        description = "Log level (DEBUG, INFO, WARN, ERROR)",
        value = "INFO",
    ),
    "flume.aws_access_key_id": dict(
        description = "AWS access key id to use S3 for storage",
        value = None,
    ),
    "flume.aws_secret_access_key": dict(
        description = "AWS secret access key to use S3 for storage",
        value = None,
    ),
}
