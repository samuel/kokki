
from kokki import *

Package("erlang")

import os
filename = url.rsplit('/', 1)[-1]
dirname = filename
while dirname.rsplit('.', 1)[-1] in ('gz', 'tar', 'tgz', 'bz2'):
    dirname = dirname.rsplit('.', 1)[0]

if not dirname:
    raise Fail("Unable to figure out directory name of project for URL %s" % url)

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
