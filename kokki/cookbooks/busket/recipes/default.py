
import os
from kokki import *

Package("erlang")

Script("install-busket",
    not_if = lambda:os.path.exists(env.config.busket.path),
    cwd = "/usr/local/src",
    code = (
        "git clone https://samuel@github.com/samuel/busket.git busket\n"
        "cd busket\n"
        "make rel\n"
        "mv rel/busket {install_path}\n"
    ).format(install_path=env.config.busket.path)
)
