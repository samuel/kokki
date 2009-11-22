
__all__ = ["Package"]

import subprocess
from pluto.base import *
from pluto.providers.package.apt import DebianAPTProvider

class Package(Resource):
    package_name = ResourceArgument()
    version = ResourceArgument()

    provider = DebianAPTProvider()

    def action_install(self):
        if not self.provider.check_installed(self.real_package_name):
            self.provider.install(self.real_package_name)
            self.changed()

    def action_upgrade(self):
        # TODO: Need to support changed
        self.provider.install(self.real_package_name)

    def action_remove(self):
        if self.provider.check_installed(self.real_package_name):
            self.provider.remove(self.real_package_name)
            self.changed()

    def action_purge(self):
        if self.provider.check_installed(self.real_package_name):
            self.provider.purge(self.real_package_name)
            self.changed()

    @property
    def real_package_name(self):
        return self.package_name or self.name
