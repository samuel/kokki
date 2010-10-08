
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
    "munin.contacts": dict(
        description = "Who to contact on alerts. List of dictionaries with keys name, email, and subject(optional).",
        default = [], # dict(name='', subject='optional', email='')
    ),
    "munin.hosts": dict(
        description = "List of hosts to monitor. List of dictionaries with keys name and ip.",
        default = [dict(name="localhost", ip="127.0.0.1")],
    ),
    "munin.dbdir": dict(
        description = "Path to directory where rrd files are kept",
        default = None, # Usually /var/lib/munin
    ),
}
