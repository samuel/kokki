
import os
import re
import subprocess
from kokki import Provider, Fail

whitespace_re = re.compile(r'\s+')

class SupervisorServiceProvider(Provider):
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

    def action_reload(self):
        self._init_cmd("update", 0)
        self.resource.updated()

    def status(self):
        p = subprocess.Popen([self.supervisorctl_path, "status"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]
        for l in out.split('\n'):
            try:
                svc, status, info = whitespace_re.split(l.strip(), 2)
                service, process_name = svc.split(':')
            except ValueError:
                continue
            if service == self.resource.service_name:
                return status.strip() == "RUNNING"
        raise Fail("Service %s not managed by supervisor" % self.resource.service_name)

    def _init_cmd(self, command, expect=None):
        ret = subprocess.call([self.supervisorctl_path, command, self.resource.service_name],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if expect is not None and expect != ret:
            raise Fail("%r command %s for service %s failed" % (self, command, self.resource.service_name))
        return ret

    @property
    def supervisorctl_path(self):
        return os.path.join(self.resource.env.config.supervisor.binary_path, "supervisorctl")
