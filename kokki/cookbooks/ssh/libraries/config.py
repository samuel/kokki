
from kokki import File, Template

def SSHConfig(name, hosts, mode=0600, **kwargs):
    File(name,
        mode = mode,
        content = Template("ssh/config.j2", {'hosts': hosts}),
        **kwargs)
