
__description__ = "SSH Service"
__config__ = {}

from kokki import *
from .providers import SSHKnownHostProvider, SSHAuthorizedKeyProvider
from .resources import SSHKnownHost, SSHAuthorizedKey

def SSHConfig(name, hosts, mode=0600, **kwargs):
    File(name,
        mode = mode,
        content = Template("ssh/config.j2", {'hosts': hosts}),
        **kwargs)
