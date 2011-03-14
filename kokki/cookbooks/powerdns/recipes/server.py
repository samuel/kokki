
from kokki import Package, Service, File, Template

Package("pdns-server")
Service("pdns")

File("/etc/powerdns/pdns.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("powerdns/pdns.conf"),
    notifies = [("reload", env.resources["Service"]["pdns"])])

for be in env.config.powerdns.backends:
    Package("pdns-backend-%s" % be)
