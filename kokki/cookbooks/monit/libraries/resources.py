
from kokki import Service, BooleanArgument

class MonitService(Service):
    provider = "*monit.MonitServiceProvider"

    supports_restart = BooleanArgument(default=True)
    supports_status = BooleanArgument(default=True)
    supports_reload = BooleanArgument(default=False)
