
__all__ = ["Package"]

import subprocess
from pluto.base import Resource

class DebianPackageProvider(object):
    def install(self, package):
        return self._dpkg("install", package)

    def remove(self, package):
        return self._dpkg("remove", package)

    def purge(self, package):
        return self._dpkg("purge", package)

    def check_installed(self, package):
        return subprocess.pcall("dpkg -s %s" % package,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def _dpkg(self, command, package):
        return subprocess.pcall("apt-get -y %s %s" % (command, package),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

class Package(Resource):
    default_action = "install"
    actions = ["install", "upgrade", "remove", "purge"]
    attributes = dict(
        package_name = None,
        version = None,
    )
    provider = DebianPackageProvider()

    def install(self):
        if not self.provider.check_installed(self.real_package_name):
            self.provider.install(self.real_package_name)
            self.changed()

    def upgrade(self):
        # TODO: Need to support changed
        self.provider.install(self.real_package_name)

    def remove(self):
        if self.provider.check_installed(self.real_package_name):
            self.provider.remove(self.real_package_name)
            self.changed()

    def purge(self):
        if self.provider.check_installed(self.real_package_name):
            self.provider.purge(self.real_package_name)
            self.changed()

    @property
    def real_package_name(self):
        return self.package_name or self.name
