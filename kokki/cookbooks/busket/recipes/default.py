
import os
from kokki import Package, File, Service, Script

Package("erlang")
# ubuntu's erlang is a bit messed up.. remove the man link
File("/usr/lib/erlang/man",
    action = "delete")

# Package("mercurial",
#     provider = "kokki.providers.package.easy_install.EasyInstallProvider")

command = os.path.join(env.config.busket.path, "bin", "busket")

Service("busket",
    start_command = "%s start" % command,
    stop_command = "%s stop" % command,
    restart_command = "{0} start || {0} restart".format(command),
    status_command = "%s ping" % command,
    action = "nothing")

Script("install-busket",
    not_if = lambda:os.path.exists(env.config.busket.path),
    cwd = "/usr/local/src",
    code = (
        "git clone git://github.com/samuel/busket.git busket\n"
        "cd busket\n"
        "mkdir /tmp/erlhome\n"
        "export HOME=/tmp/erlhome\n"
        "make release\n"
        "mv rel/busket {install_path}\n"
    ).format(install_path=env.config.busket.path),
    notifies = [("start", env.resources["Service"]["busket"])],
)

if "librato.silverline" in env.included_recipes:
    File("/etc/default/busket",
        owner = "root",
        group = "root",
        mode = 0644,
        content = (
            'RUNNER_ENV="SL_NAME=busket"\n'
        ),
        notifies = [("restart", env.resources["Service"]["busket"])])
