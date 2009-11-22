
__all__ = ["Service"]

import subprocess

from pluto.base import Resource, Fail

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
        if expect is not None and expect != res:
            raise Fail("%r command %s for service %s failed" % (self, command, service_name))
        return ret

class Service(Resource):
    default_action = "nothing"
    actions = ["enable", "disable", "start", "stop", "restart", "reload"]
    attributes = dict(
        service_name = None,
        enabled = None,
        running = None,
        pattern = None,
        start_command = None,
        stop_command = None,
        status_command = None,
        restart_command = None,
        reload_command = None,
        supports_restart = False,
        supports_reload = False,
        supports_status = False,
    )
    provider = DebianServiceProvider()

    def start(self):
        service = self.service_name or self.name
        if not self.provider.status(service):
            self.provider.start(service)
            self.changed()

    def stop(self):
        service = self.service_name or self.name
        if self.provider.status(service):
            self.provider.stop(service)
            self.changed()

    def restart(self):
        self.provider.restart(self.service_name or self.name)

    def reload(self):
        self.provider.reload(self.service_name or self.name)
