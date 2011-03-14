
from kokki import Package, Directory, File, Template

Package("munin")

Directory(env.config.munin.dbdir,
    owner = "munin",
    group = "munin",
    mode = 0755)

File("/etc/munin/munin.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("munin/munin.conf.j2"))
