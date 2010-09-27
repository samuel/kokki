
from kokki import *

include_recipe("monit")

Package("supervisor",
    provider = "kokki.providers.package.easy_install.EasyInstallProvider")

File("supervisord.conf",
    path = "%s/supervisord.conf" % env.supervisor.config_path,
    content = Template("supervisor/supervisord.conf.j2"))

Directory("supervisor.d",
    path = "%s/supervisor.d" % env.supervisor.config_path)

cookbook.monit.monitrc("supervisord",
    content = Template("supervisor/monit.conf.j2"))

cookbooks.monit.MonitService("supervisord",
    subscribes = [("restart", env.resources["File"]["supervisord.conf"])])
