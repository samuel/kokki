
__all__ = ["Service"]

import subprocess

from pluto.base import *

class DebianServiceProvider(object):
    def start(self, service_name):
        self._init_cmd(service_name, "start", 0)

    def stop(self, service_name):
        self._init_cmd(service_name, "stop", 0)

    def restart(self, service_name):
        self._init_cmd(service_name, "restart", 0)

    def reload(self, service_name):
        self._init_cmd(service_name, "reload", 0)

    def status(self, service_name):
        return self._init_cmd(service_name, "status") == 0

    def _init_cmd(self, service_name, command, expect=None):
        ret = subprocess.call(["/etc/init.d/%s" % service_name, command],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if expect is not None and expect != ret:
            raise Fail("%r command %s for service %s failed" % (self, command, service_name))
        return ret

class Service(Resource):
    service_name = ResourceArgument()
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

    provider = DebianServiceProvider()

    def action_start(self):
        service = self.service_name or self.name
        if not self.provider.status(service):
            self.provider.start(service)
            self.changed()

    def action_stop(self):
        service = self.service_name or self.name
        if self.provider.status(service):
            self.provider.stop(service)
            self.changed()

    def action_restart(self):
        self.provider.restart(self.service_name or self.name)

    def action_reload(self):
        self.provider.reload(self.service_name or self.name)
