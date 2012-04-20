
import os
from kokki import Package, File, Directory, Service, Template, Link

# env.include_recipe("monit")

if env.system.platform == "ubuntu":
	Package("supervisor")
else:
	Package("supervisor",
		provider = "kokki.providers.package.easy_install.EasyInstallProvider")
	Directory(os.path.dirname(env.config.supervisor.config_path),
		action = "create")
	Directory(env.config.supervisor.custom_config_path,
		action = "create")
	Directory(os.path.dirname(env.config.supervisor.pidfile),
		action = "create")
	Directory(os.path.dirname(env.config.supervisor.logfile),
		action = "create")
	Directory(env.config.supervisor.childlogdir,
		action = "create")
	if env.config.supervisor.config_path != "/etc/supervisord.conf":
		Link("/etc/supervisord.conf",
			to = env.config.supervisor.config_path)

File("supervisord.conf",
    path = env.config.supervisor.config_path,
    content = Template("supervisor/supervisord.conf.j2"))

Directory("supervisor.d",
    path = env.config.supervisor.custom_config_path)

supervisorctl = os.path.join(env.config.supervisor.binary_path, "supervisorctl")
Service("supervisor",
    restart_command = "%s reload" % supervisorctl,
    reload_command = "%s update" % supervisorctl,
    subscribes = [("reload", env.resources["File"]["supervisord.conf"])])

#env.cookbooks.monit.rc("supervisord",
#    content = Template("supervisor/monit.conf.j2"))

#env.cookbooks.monit.MonitService("supervisord",
#    subscribes = [("restart", env.resources["File"]["supervisord.conf"])])
