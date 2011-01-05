
import logging
import re
from subprocess import Popen, STDOUT, PIPE
from kokki.base import Fail
from kokki.providers import Provider

class PackageProvider(Provider):
    def __init__(self, *args, **kwargs):
        super(PackageProvider, self).__init__(*args, **kwargs)
        self.get_current_status()

    def action_install(self):
        if self.resource.version != None and self.resource.version != self.current_version:
            install_version = self.resource.version
        elif self.current_version is None:
            install_version = self.candidate_version
        else:
            return

        if not install_version:
            raise Fail("No version specified, and no candidate version available.")

        self.log.info("Install %s version %s (resource %s, current %s, candidate %s)" %
            (self.resource.package_name, install_version, self.resource.version, self.current_version, self.candidate_version))

        status = self.install_package(self.resource.package_name, install_version)
        if status:
            self.resource.updated()

    def action_upgrade(self):
        if self.current_version != self.candidate_version:
            orig_version = self.current_version or "uninstalled"
            self.log.info("Upgrading %s from version %s to %s" % (self.resource, orig_version, self.candidate_version))

            status = self.upgrade_package(self.resource.package_name, self.candidate_version)
            if status:
                self.resource.updated()

    def action_remove(self):
        if self.current_version:
            self.log.info("Remove %s version %s" % (self.resource.package_name, self.current_version))
            self.remove_package(self.resource.package_name)
            self.resource.updated()

    def action_purge(self):
        if self.current_version:
            self.log.info("Purging %s version %s" % (self.resource.package_name, self.current_version))
            self.purge_package(self.resource.package_name)
            self.resource.updated()
