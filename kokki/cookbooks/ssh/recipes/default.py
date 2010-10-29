
from kokki import *

if env.system.os == "linux":
    Package("openssh-server", action="upgrade")
    Package("openssh-client", action="upgrade")

    Service("ssh")

    File("sshd_config",
        path = "/etc/ssh/sshd_config",
        content = Template("ssh/sshd_config.j2"),
        mode = 0644,
        owner = "root",
        group = "root",
        notifies = [("restart", env.resources["Service"]["ssh"], True)]
    )