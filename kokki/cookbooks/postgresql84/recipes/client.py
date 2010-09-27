
from kokki import *

if env.system.platform in ("ubuntu", "debian"):
    Package("postgresql-client")
elif env.system.platform in ("redhat", "centos", "fedora"):
    Package("postgresql-devel")
else:
    raise Fail("Unsupported platform %s for recipe postgresql.client" % env.system.platform)
