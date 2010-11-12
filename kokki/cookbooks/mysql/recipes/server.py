
from kokki import *

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
    supports_restart = True,
    action = "start")

# File("/etc/mysql/my.cnf",
#     owner = "root",
#     group = "root",
#     mode = 0644,
#     content = Template("mysql/my.cnf.j2"),
#     notifies = [("restart", env.resources["Service"]["mysql"], True)])

Execute("mysql_install_db --user=mysql --datadir=%s" % env.config.datadir,
    creates = env.config.datadir)

File("/etc/mysql/conf.d/kokki.cnf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("mysql/kokki.cnf.j2"),
    notifies = [("restart", env.resources["Service"]["mysql"], True)])

# grants_path = value_for_platform(
#   ["centos", "redhat", "suse", "fedora" ] => {
#     "default" => "/etc/mysql_grants.sql"
#   },
#   "default" => "/etc/mysql/grants.sql"
# )
# 
# begin
#   t = resources(:template => "/etc/mysql/grants.sql")
# rescue
#   Chef::Log.warn("Could not find previously defined grants.sql resource")
#   t = template "/etc/mysql/grants.sql" do
#     path grants_path
#     source "grants.sql.erb"
#     owner "root"
#     group "root"
#     mode "0600"
#     action :create
#   end
# end
# 
# execute "mysql-install-privileges" do
#   command "/usr/bin/mysql -u root #{node[:mysql][:server_root_password].empty? ? '' : '-p' }#{node[:mysql][:server_root_password]} < #{grants_path}"
#   action :nothing
#   subscribes :run, resources(:template => "/etc/mysql/grants.sql"), :immediately
# end
