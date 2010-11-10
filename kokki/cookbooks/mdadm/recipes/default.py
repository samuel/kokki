
from kokki import *

if env.config.mdadm.arrays:
    Package("mdadm")

for array in env.config.mdadm.arrays:
    pass
