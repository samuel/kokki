
import subprocess
from kokki import *

class MonitServiceProvider(Provider):
    def action_start(self):
        if not self.status():
            self._init_cmd("start", 0)
            self.resource.updated()

    def action_stop(self):
        if self.status():
            self._init_cmd("stop", 0)
            self.resource.updated()

    def action_restart(self):
        self._init_cmd("restart", 0)
        self.resource.updated()

    def status(self):
        p = subprocess.Popen(["/usr/sbin/monit", "summary"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]
        for l in out.split('\n'):
            try:
                typ, name, status = l.strip().split(' ', 2)
            except ValueError:
                continue
            if typ.strip() == 'Process' and name.strip() == "'%s'" % self.resource.service_name:
                return status.strip() == "running"
        raise Fail("Service %s not managed by monit" % self.resource.service_name)

    def _init_cmd(self, command, expect=None):
        ret = subprocess.call(["/usr/sbin/monit", command, self.resource.service_name],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if expect is not None and expect != ret:
            raise Fail("%r command %s for service %s failed" % (self, command, self.resource.service_name))
        return ret
