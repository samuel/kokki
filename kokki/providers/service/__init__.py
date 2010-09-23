import os
import subprocess

from kokki.base import Fail
from kokki.providers import Provider

class ServiceProvider(Provider):
    def action_start(self):
        if not self.status():
            self._init_cmd("start", 0)
            self.resource.updated()

    def action_stop(self):
        if self.status():
            self._init_cmd("stop", 0)
            self.resource.updated()

    def action_restart(self):
        if not self.status():
            self._init_cmd("start", 0)
            self.resource.updated()
        else:
            self._init_cmd("restart", 0)
            self.resource.updated()

    def action_reload(self):
        if not self.status():
            self._init_cmd("start", 0)
            self.resource.updated()
        else:
            self._init_cmd("reload", 0)
            self.resource.updated()

    def status(self):
        return self._init_cmd("status") == 0

    def _init_cmd(self, command, expect=None):
        if command != "status":
            self.log.info("%s command '%s'" % (self.resource, command))
        custom_cmd = getattr(self.resource, "%s_command" % command, None)
        if custom_cmd:
            self.log.debug("%s executing '%s'" % (self.resource, custom_cmd))
            ret = subprocess.call(custom_cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif self._upstart:
            p = subprocess.Popen(["/sbin/"+command, self.resource.service_name],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = p.communicate()[0]
            proc, state = out.strip().split(' ', 1)
            ret = 0 if state != "stop/waiting" else 1
        else:
            ret = subprocess.call(["/etc/init.d/%s" % self.resource.service_name, command],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if expect is not None and expect != ret:
            raise Fail("%r command %s for service %s failed" % (self, command, self.resource.service_name))
        return ret

    @property
    def _upstart(self):
        try:
            return self.__upstart
        except AttributeError:
            self.__upstart = os.path.exists("/sbin/start")
        return self.__upstart
