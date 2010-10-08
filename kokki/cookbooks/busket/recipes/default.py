
import os
from kokki import *

Package("erlang")

Package("mercurial",
    provider = "kokki.providers.package.easy_install.EasyInstallProvider")

Script("install-busket",
    not_if = lambda:os.path.exists(env.config.busket.path),
    cwd = "/usr/local/src",
    code = (
        "git clone git://github.com/samuel/busket.git busket\n"
        "cd busket\n"
        "make release\n"
        "mv rel/busket {install_path}\n"
    ).format(install_path=env.config.busket.path)
)
