
import re
from subprocess import Popen, STDOUT, PIPE, check_call
from pluto.base import Fail
from pluto.providers.package import PackageProvider

class DebianAptProvider(PackageProvider):
    def get_current_status(self):
        p = Popen("apt-cache policy %s" % self.resource.package_name, shell=True, stdout=PIPE)
        out = p.communicate()[0]
        for line in out.split("\n"):
            line = line.strip().split(':', 1)
            if len(line) != 2:
                continue

            v = line[1].strip()
            if line[0] == "Installed":
                self.current_version = None if v == '(none)' else v
                self.log.debug("Current version of package %s is %s" % (self.resource.package_name, self.current_version))
            elif line[0] == "Candidate":
                self.candidate_version = v

        if self.candidate_version == "(none)":
            raise Fail("APT does not provide a version of package %s" % package)

    def install_package(self, name, version):
        return 0 == check_call("DEBIAN_FRONTEND=noninteractive apt-get -q -y install %s=%s" % (name, version),
            shell=True, stdout=PIPE, stderr=STDOUT)

    def upgrade_package(self, name, version):
        return self.install_package(name, version)
