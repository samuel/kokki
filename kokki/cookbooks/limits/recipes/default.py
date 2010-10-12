
from kokki import *

File("/etc/security/limits.conf",
    owner = "root",
    group = "root",
    mode = 0644,
    content = Template("limits/limits.conf.j2"))
