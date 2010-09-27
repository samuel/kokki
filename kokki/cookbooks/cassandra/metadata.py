
__description__ = "Cassandra database"
__config__ = {
    "cassandra.cluster_name": dict(
        display_name = "Cassandra cluster name",
        description = "Name of the Cassandra cluster",
        default = "Test Cluster",
    ),
    "cassandra.auto_bootstrap": dict(
        display_name = "Auto bootstrap",
        description = "Turns on or off the auto-bootstrapping of the node",
        default = False,
    ),
    "cassandra.hinted_handoff_enabled": dict(
        display_name = "Hinted hand-off enabled",
        description = "Enable or disable hinted hand-off",
        default = True,
    ),
    "cassandra.partitioner": dict(
        display_name = "Partitioner",
        description = "Partitioner class path",
        default = "org.apache.cassandra.dht.RandomPartitioner",
    ),
    "cassandra.data_file_directories": dict(
        display_name = "Data file directories",
        description = "List of directories where Cassandra should store data on disk",
        default = ['/var/lib/cassandra/data'],
    ),
    "cassandra.seeds": dict(
        display_name = "Seed nodes",
        description = "List of addresses for seed nodes",
        default = ['127.0.0.1'],
    ),
    "cassandra.disk_access_mode": dict(
        display_name = "Disk access mode",
        description = "How Cassandra handles i/o (auto, mmap, mmap_index_only, or standard)",
        default = "auto",
    ),
    "cassandra.listen_address": dict(
        display_name = "Listen address",
        description = "Address to bind to and tell other nodes to connect to",
        default = "127.0.0.1",
    ),
    "cassandra.rpc_address": dict(
        display_name = "RPC Address",
        description = "Address to bind the Thrift RPC to",
        default = "127.0.0.1",
    ),
    "cassandra.commitlog_directory": dict(
        display_name = "Commit log directory",
        description = "Path where to store the commit log",
        default = "/var/lib/cassandra/commitlog",
    ),
    "cassandra.endpoint_snitch": dict(
        display_nane = "End-point snitch",
        description = "Class that will Cassandra discover topology of the network",
        default = "org.apache.cassandra.locator.SimpleSnitch",
    ),
}
