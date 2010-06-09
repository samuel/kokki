
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

        self.log.info("Install %s version %s" % (self.resource.package_name, install_version))

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
      
      # def action_remove        
      #   if should_remove_package(@current_resource.version, @new_resource.version)
      #     Chef::Log.info("Removing #{@new_resource}")
      #     remove_package(@current_resource.package_name, @new_resource.version)
      #     @new_resource.updated = true
      #   end
      # end
      # 
      # def should_remove_package(current_version, new_version)
      #   to_remove_package = false
      #   if current_version != nil
      #     if new_version != nil 
      #       if new_version == current_version
      #         to_remove_package = true
      #       end
      #     else
      #       to_remove_package = true
      #     end
      #   end
      #   to_remove_package
      # end
      # 
      # def action_purge
      #   if should_remove_package(@current_resource.version, @new_resource.version)
      #     Chef::Log.info("Purging #{@new_resource}")
      #     purge_package(@current_resource.package_name, @new_resource.version)
      #     @new_resource.updated = true
      #   end
      # end
      # 
