
__description__ = "Data flows"
__config__ = {
    "flume.master.servers": dict(
        description = "Address for the config servers status server (http)",
        default = None,
    ),
    "flume.plugin.classes": dict(
        description = "Comma separated list of plugin classes",
        default = None,
    ),
    "flume.collector.event.host": dict(
        description = "Host name of the default 'remote' colelctor",
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
 }
