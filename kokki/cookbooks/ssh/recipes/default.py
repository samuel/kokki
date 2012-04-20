
from kokki import Service, Package, File, Template

if env.system.os == "linux":
    Package("openssh-server", action="upgrade")
    Package("openssh-client", action="upgrade")

    if not env.config.ssh.service_name:
        if env.system.platform in ("redhat", "fedora", "centos", "amazon"):
            env.config.ssh.service_name = "sshd"
        else:
            env.config.ssh.service_name = "ssh"

    Service("ssh",
        service_name = env.config.ssh.service_name)

    File("sshd_config",
        path = "/etc/ssh/sshd_config",
        content = Template("ssh/sshd_config.j2"),
        mode = 0644,
        owner = "root",
        group = "root",
        notifies = [("restart", env.resources["Service"]["ssh"], True)]
    )