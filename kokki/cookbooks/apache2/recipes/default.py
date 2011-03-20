
from kokki import Package, Directory, Service, File, StaticFile, Execute, Template

PLATFORM_CONFIGS = dict(
    centos = "httpd",
    redhat = "httpd",
    fedora = "httpd",
    suse = "httpd",
    debian = "apache2",
    ubuntu = "apache2",
)

Package("apache2",
    package_name = "httpd" if env.system.platform in ("centos", "redhat", "fedora", "suse") else "apache2")

Directory(env.config.apache.log_dir, mode = 0700, owner = env.config.apache.user, group = env.config.apache.user)

if env.system.platform in ("centos", "redhat", "fedora", "suse"):
    Service("apache2",
        service_name = "httpd",
        restart_command = "/sbin/service httpd restart && sleep 1",
        reload_command = "/sbin/service httpd reload && sleep 1",
        supports_restart = True,
        supports_reload = True,
        supports_status = True)

    File("/usr/local/bin/apache2_module_conf_generate.pl",
        mode = 0755,
        owner = "root",
        group = "root",
        content = StaticFile("apache2/files/apache2_module_conf_generate.pl"))

    for d in ('sites-available', 'sites-enabled', 'mods-available', 'mods-enabled'):
        Directory("%s/%s" % (env.config.apache.dir, d),
            mode = 0755,
            owner = "root",
            group = "root")

    libdir = "lib64" if env.system.architecture == "x86_64" else "lib"
    Execute("generate-module-list",
        command = "/usr/local/bin/apache2_module_conf_generate.pl /usr/%s/httpd/modules /etc/httpd/mods-available" % libdir)

    # %w{a2ensite a2dissite a2enmod a2dismod}.each do |modscript|
    # template "/usr/sbin/#{modscript}" do
    #   source "#{modscript}.erb"
    #   mode 0755
    #   owner "root"
    #   group "root"
    # end  
    # end
    # 
    # # installed by default on centos/rhel, remove in favour of mods-enabled
    # file "#{node[:apache][:dir]}/conf.d/proxy_ajp.conf" do
    # action :delete
    # backup false
    # end
    # file "#{node[:apache][:dir]}/conf.d/README" do
    # action :delete
    # backup false
    # end
    # 
    # # welcome page moved to the default-site.rb temlate
    # file "#{node[:apache][:dir]}/conf.d/welcome.conf" do
    # action :delete
    # backup false
    # end
else: # debian, ubuntu
    Service("apache2",
        supports_restart = True,
        supports_reload = True,
        supports_status = True)

Directory("%s/ssl" % env.config.apache.dir,
    mode = 0755,
    owner = "root",
    group = "root")

File("apache2.conf",
    path = ("%s/conf/httpd.conf" if env.system.platform in ("centos", "redhat", "fedora") else "%s/apache2.conf") % env.config.apache.dir,
    content = Template("apache2/apache2.conf.j2"),
    owner = "root",
    group = "root",
    mode = 0644,
    notifies = [("restart", env.resources["Service"]["apache2"])])

File("apache2-security",
    path = "%s/conf.d/security" % env.config.apache.dir,
    content = Template("apache2/security.j2"),
    owner = "root",
    group = "root",
    mode = 0644,
    notifies = [("restart", env.resources["Service"]["apache2"])])

File("apache2-charset",
    path = "%s/conf.d/charset" % env.config.apache.dir,
    content = Template("apache2/charset.j2"),
    owner = "root",
    group = "root",
    mode = 0644,
    notifies = [("restart", env.resources["Service"]["apache2"])])
 
File("apache2-ports.conf",
    path = "%s/ports.conf" % env.config.apache.dir,
    content = Template("apache2/ports.conf.j2"),
    owner = "root",
    group = "root",
    mode = 0644,
    notifies = [("restart", env.resources["Service"]["apache2"])])

# File("apache2-default",
#     path = "%s/sites-available/default" % env.config.apache.dir,
#     content = Template("apache2/default-site.j2"),
#     owner = "root",
#     group = "root",
#     mode = 0644,
#     noifies = [("restart", env.resources["Service"]["apache2"])])
 
File("apache2-default-000",
    path = "%s/sites-enabled/000-default" % env.config.apache.dir,
    action = "delete")

env.cookbooks.apache2.module("alias", conf=False)

# env.cookbooks.apache2.module("status", conf=True)
# include_recipe "apache2::mod_status"
# include_recipe "apache2::mod_alias"
# include_recipe "apache2::mod_auth_basic"
# include_recipe "apache2::mod_authn_file"
# include_recipe "apache2::mod_authz_default"
# include_recipe "apache2::mod_authz_groupfile"
# include_recipe "apache2::mod_authz_host"
# include_recipe "apache2::mod_authz_user"
# include_recipe "apache2::mod_autoindex"
# include_recipe "apache2::mod_dir"
# include_recipe "apache2::mod_env"
# include_recipe "apache2::mod_mime"
# include_recipe "apache2::mod_negotiation"
# include_recipe "apache2::mod_setenvif"
# include_recipe "apache2::mod_log_config" if platform?("centos", "redhat", "suse")
