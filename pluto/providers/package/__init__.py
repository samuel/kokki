
import logging
import re
from subprocess import Popen, STDOUT, PIPE
from pluto.base import Fail
from pluto.providers import Provider

class PackageProvider(Provider):
    def __init__(self, *args, **kwargs):
        super(PackageProvider, self).__init__(*args, **kwargs)
        self.candidate_version = None
        self.get_current_status()

    def action_install(self):
        if self.resource.version != None and self.resource.version != self.current_version:
            install_version = self.resource.version
        elif self.current_version is None:
            install_version = self.candidate_version
        else:
            return

        if not install_version:
            raise Fail("No verison specified, and no candidate verison available.")

        self.log.info("Install %s version %s" % (self.resource.package_name, install_version))

        status = self.install_package(self.resource.package_name, install_version)
        if status:
            self.resource.updated()
