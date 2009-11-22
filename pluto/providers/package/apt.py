
import re
from subprocess import Popen, STDOUT, PIPE

class DebianAPTProvider(object):
    def get_current_status(self, package):
        if not hasattr(self, '_status'):
            p = Popen("apt-cache policy %s" % package, shell=True, stdout=PIPE)
            out = p.community()[0]
            status = {}
            for line in out.split("\n"):
                line = line.strip().split(':')
                v = line[1].strip()
                if line[0] == "Installed":
                    status['installed'] = None if v == '(none)' else v
                elif line[0] == "Candidate":
                    status['candidate'] = v
            if status['candidate'] == "(none)":
                raise Exception("APT does not provide a version of package %s" % package)
            self._status = status
        return self._status

    def install(self, package):
        return self._aptget("install", package)

    def remove(self, package):
        return self._aptget("remove", package)

    def purge(self, package):
        return self._aptget("purge", package)

    def check_installed(self, package):
        return bool(self.get_current_status()['installed'])

    def _aptget(self, command, package):
        return subprocess.check_call("apt-get -q -y %s %s" % (command, package),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
