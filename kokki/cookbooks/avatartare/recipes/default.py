
import os
from kokki import Package, Directory, Execute, File, Template

env.include_recipe("mongodb")
env.include_recipe("supervisor")

env.cookbooks.supervisor.SupervisorService("avatartare")

Package("python-pycurl")
Package("python-imaging")

# Clone project
Directory(os.path.dirname(env.config.avatartare.path), mode=0755)
Execute("git clone git://github.com/samuel/avatartare.git %s" % env.config.avatartare.path,
    creates = env.config.avatartare.path,
)

# Bootstrap the environment
Execute("avatartare-bootstrap",
    command = "python bin/bootstrap.py env",
    cwd = env.config.avatartare.path,
    creates = "%s/env" % env.config.avatartare.path,
)

# Config
File("avatartare-local_settings.py",
    path = "%s/local_settings.py" % env.config.avatartare.path,
    content = Template("avatartare/local_settings.py.j2"),
    notifies = [("restart", env.resources["SupervisorService"]["avatartare"])])

# Setup Supervisor to start and monitor the processes
File("%s/avatartare.conf" % env.config.supervisor.custom_config_path,
    content = Template("avatartare/supervisor.j2"),
    notifies = [("restart", env.resources["SupervisorService"]["avatartare"])])
