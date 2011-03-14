
from kokki import Package, File, Template

Package("sudo", action="upgrade")
File("/etc/sudoers",
    owner = "root",
    group = "root",
    mode = 0440,
    content = Template("sudo/sudoers.j2"),
)
