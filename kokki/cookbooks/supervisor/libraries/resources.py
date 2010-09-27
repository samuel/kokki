
from kokki import *

class SupervisorService(Service):
    provider = "*supervisor.SupervisorServiceProvider"

    supports_restart = BooleanArgument(default=True)
    supports_status = BooleanArgument(default=True)
    supports_reload = BooleanArgument(default=True)
