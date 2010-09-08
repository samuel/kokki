
from kokki import *

if env.system.os == "linux":
    Package("openssh-server", action="upgrade")
    Package("openssh-client", action="upgrade")
