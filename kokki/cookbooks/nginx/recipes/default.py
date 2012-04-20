
from kokki import Package, Directory, File, Template, Service

if not env.config.nginx.user:
    if env.system.platform == "amazon":
        env.config.nginx.user = "nginx"
    else:
        env.config.nginx.user = "www-data"

Package("nginx")

Directory(env.config.nginx.log_dir,
    mode = 0755,
    owner = env.config.nginx.user,
    action = 'create')

for nxscript in ('nxensite', 'nxdissite'):
    File("/usr/sbin/%s" % nxscript,
        content = Template("nginx/%s.j2" % nxscript),
        mode = 0755,
        owner = "root",
        group = "root")

File("nginx.conf",
    path = "%s/nginx.conf" % env.config.nginx.dir,
    content = Template("nginx/nginx.conf.j2"),
    owner = "root",
    group = "root",
    mode = 0644)

Directory("%s/sites-available" % env.config.nginx.dir,
    mode = 0755,
    owner = env.config.nginx.user,
    action = "create")

Directory("%s/sites-enabled" % env.config.nginx.dir,
    mode = 0755,
    owner = env.config.nginx.user,
    action = "create")

File("%s/sites-available/default" % env.config.nginx.dir,
    content = Template("nginx/default-site.j2"),
    owner = "root",
    group = "root",
    mode = 0644)

Service("nginx",
    supports_status = True,
    supports_restart = True,
    supports_reload = True,
    action = "start",
    subscribes = [("reload", env.resources["File"]["nginx.conf"])])

if "librato.silverline" in env.included_recipes:
    File("/etc/default/nginx",
        owner = "root",
        group = "root",
        mode = 0644,
        content = (
            "export SL_NAME=nginx\n"
        ),
        notifies = [("restart", env.resources["Service"]["nginx"])])
