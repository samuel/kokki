
from kokki import Package, Directory, Link, File, Template

env.include_recipe("cloudera")

Package("flume")

Directory("/etc/flume/conf.kokki",
    owner = "root",
    group = "root",
    mode = 0755)

Link("/etc/flume/conf",
    to = "/etc/flume/conf.kokki")

File("flume-config",
    path = "/etc/flume/conf.kokki/flume-conf.xml",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("flume/flume-conf.xml.j2"))

File("flume-site-config",
    path = "/etc/flume/conf.kokki/flume-site.xml",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("flume/flume-site.xml.j2"))

File("flume-log-config",
    path = "/etc/flume/conf.kokki/log4j.properties",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("flume/log4j.properties.j2"))

File("flume-daemon-sh",
    path = "/usr/lib/flume/bin/flume-daemon.sh",
    owner = "root",
    group = "root",
    mode = 0755,
    content = Template("flume/flume-daemon.sh.j2"))

Directory(env.config.flume.agent.logdir,
    owner = "flume",
    group = "flume",
    recursive = True)

Directory(env.config.flume.master.zk.logdir,
    owner = "flume",
    group = "flume",
    recursive = True)
