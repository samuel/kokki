
import os
from kokki import Execute, File

base_url = "http://aspersa.googlecode.com/svn/trunk/{name}"

for name in env.config.aspersa.scripts:
    path = os.path.join(env.config.aspersa.install_path, name)
    url = base_url.format(name=name)
    Execute("wget -q -O {path} {url}".format(path=path, url=url),
        creates = path)
    File(path,
        owner = "root",
        group = "root",
        mode = 0755)
