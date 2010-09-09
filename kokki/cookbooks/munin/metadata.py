
__description__ = "Munin and munin-node server monitoring"
__config__ = {
    "munin.bind": dict(
        description = "IP address munin-node should bind to",
        default = "127.0.0.1",
    ),
    "munin.port": dict(
        description = "Port number munin-node should listen on",
        default = 4949,
    ),
    "munin.allow": dict(
        description = "IP address ranges that are allowed to connect to munin-node",
        default = ["127.0.0.1/32"],
    ),
}
