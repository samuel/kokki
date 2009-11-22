
import re
from subprocess import Popen, STDOUT, PIPE
from pluto.base import Fail
from pluto.providers.package import PackageProvider

class DebianAptProvider(PackageProvider):
    def get_current_status(self):
        p = Popen("apt-cache policy %s" % self.resource.package_name, shell=True, stdout=PIPE)
        out = p.communicate()[0]
        for line in out.split("\n"):
            line = line.strip().split(':')
            v = line[1].strip()
            if line[0] == "Installed":
                self.current_version = None if v == '(none)' else v
                self.log.debug("Current version of package %s is %s" % (current.package_name, current.version))
            elif line[0] == "Candidate":
                self.candidate_version = v

        if self.candidate_version == "(none)":
            raise Fail("APT does not provide a version of package %s" % package)

    def install_package(self, name, version):
        return subprocess.check_call("apt-get -q -y install %s=%s" % (command, name, version),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # def action_upgrade(self):
    #     # TODO: Need to support changed
    #     self.provider.install(self.real_package_name)
    # 
    # def action_remove(self):
    #     if self.provider.check_installed(self.real_package_name):
    #         self.provider.remove(self.real_package_name)
    #         self.changed()
    # 
    # def action_purge(self):
    #     if self.provider.check_installed(self.real_package_name):
    #         self.provider.purge(self.real_package_name)
    #         self.changed()
    # 
    # def action_install(self, package):
    #     if not self.check_installed(package):
    #         return self._aptget("install", package)
    # 
    # def action_remove(self, package):
    #     return self._aptget("remove", package)
    # 
    # def action_purge(self, package):
    #     return self._aptget("purge", package)
    # 
    # def check_installed(self, package):
    #     return bool(self.get_current_status()['installed'])
