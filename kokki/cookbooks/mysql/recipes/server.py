
from kokki import Directory, Execute, File, Template, Package, Service

env.include_recipe("mysql.client")

if env.system.platform in ("debian", "ubuntu"):
    Directory("/var/cache/local/preseeding",
        owner = "root",
        group = "root",
        mode = 0755,
        recursive = True)

    Execute("preseed mysql-server",
        command = "debconf-set-selections /var/cache/local/preseeding/mysql-server.seed",
        action = "nothing")

    File("/var/cache/local/preseeding/mysql-server.seed",
        owner = "root",
        group = "root",
        mode = 0600,
        content = Template("mysql/mysql-server.seed.j2"),
        notifies = [("run", env.resources["Execute"]["preseed mysql-server"], True)])

    File("/etc/mysql/debian.cnf",
        owner = "root",
        group = "root",
        mode = 0600,
        content = Template("mysql/debian.cnf.j2"))

Package("mysql-server")
Service("mysql",
    supports_status = True,
    supports_restart = True)

Execute("mysql_install_db --user=mysql --datadir=%s" % env.config.mysql.datadir,
    creates = env.config.mysql.datadir)

File("/etc/mysql/conf.d/kokki.cnf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("mysql/kokki.cnf.j2"),
    notifies = [("restart", env.resources["Service"]["mysql"], True)])

File("/etc/mysql/grants.sql",
    owner = "root",
    group = "root",
    mode = 0600,
    content = Template("mysql/grants.sql.j2"))

Execute("/usr/bin/mysql -u root --password='%s' < /etc/mysql/grants.sql" % env.config.mysql.server_root_password,
    action = "nothing",
    subscribes = [("run", env.resources["File"]["/etc/mysql/grants.sql"], True)])
