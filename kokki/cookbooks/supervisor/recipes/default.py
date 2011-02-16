
import os
from kokki import *

env.include_recipe("monit")

Package("supervisor")
#    provider = "kokki.providers.package.easy_install.EasyInstallProvider")

File("supervisord.conf",
    path = "%s/supervisord.conf" % env.config.supervisor.config_path,
    content = Template("supervisor/supervisord.conf.j2"))

Directory("supervisor.d",
    path = "%s/supervisor.d" % env.config.supervisor.config_path)

Service("supervisor",
    reload_command = os.path.join(env.config.supervisor.binary_path, "supervisorctl") + " update",
    subscribes = [("restart", env.resources["File"]["supervisord.conf"])])

#env.cookbooks.monit.rc("supervisord",
#    content = Template("supervisor/monit.conf.j2"))

#env.cookbooks.monit.MonitService("supervisord",
#    subscribes = [("restart", env.resources["File"]["supervisord.conf"])])
