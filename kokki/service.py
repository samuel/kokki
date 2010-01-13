
__all__ = ["Service"]

from kokki.base import *

class Service(Resource):
    service_name = ResourceArgument(default=lambda obj:obj.name)
    enabled = ResourceArgument()
    running = ResourceArgument()
    pattern = ResourceArgument()
    start_command = ResourceArgument()
    stop_command = ResourceArgument()
    status_command = ResourceArgument()
    restart_command = ResourceArgument()
    reload_command = ResourceArgument()
    supports_restart = BooleanArgument(default=False)
    supports_reload = BooleanArgument(default=False)
    supports_status = BooleanArgument(default=False)

    actions = ["nothing", "start", "stop", "restart", "reload"]
