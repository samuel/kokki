
from kokki import Package, File, Template, Directory, Service

Package("monit")

File("%s/monitrc" % env.config.monit.config_path,
    owner = "root",
    group = "root",
    mode = 0700,
    content = Template("monit/monitrc.j2"))

if env.system.platform == "ubuntu":
    File("/etc/default/monit",
        content = Template("monit/default.j2"))

Directory("%s/monit.d" % env.config.monit.config_path,
    owner = "root",
    group = "root",
    mode = 0700)

Directory("/var/monit",
    owner = "root",
    group = "root",
    mode = 0700)

Service("monit",
    supports_restart = True,
    supports_status = False,
    subscribes = [('restart', env.resources['File']["%s/monitrc" % env.config.monit.config_path])])
