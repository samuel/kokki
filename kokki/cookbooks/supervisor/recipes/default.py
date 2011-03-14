
import os
from kokki import Package, File, Directory, Service, Template

# env.include_recipe("monit")

Package("supervisor")
#    provider = "kokki.providers.package.easy_install.EasyInstallProvider")

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
