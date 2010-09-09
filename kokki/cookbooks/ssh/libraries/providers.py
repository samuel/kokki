
__all__ = ["SSHKnownHostProvider", "SSHAuthorizedKeyProvider"]

import os
import re
import subprocess
from kokki import *

class SSHKnownHostProvider(Provider):
    def action_include(self):
        hosts = SSHKnownHostsFile(self.resource.path)
        modified = False
        for host in self.resource.host.split(','):
            if hosts.add_host(host, self.resource.keytype, self.resource.key, hashed=self.resource.hashed):
                modified = True
                self.log.info("[%s] Added host %s to known_hosts file %s" % (self, host, self.resource.path))
            else:
                self.log.debug("[%s] Host %s already in known_hosts file %s" % (self, host, self.resource.path))
        if modified:
            hosts.save(self.resource.path)
            self.resource.updated()

    def action_exclude(self):
        hosts = SSHKnownHostsFile(self.resource.path)
        modified = False
        for host in self.resource.host.split(','):
            if hosts.remove_host(host):
                modified = True
                self.log.info("[%s] Removed host %s from known_hosts file %s" % (self, host, self.resource.path))
            else:
                self.log.debug("[%s] Host %s not found in known_hosts file %s" % (self, host, self.resource.path))
        if modified:
            hosts.save(self.resource.path)
            self.resource.updated()

class SSHAuthorizedKeyProvider(Provider):
    def action_include(self):
        keys = SSHAuthorizedKeysFile(self.resource.path)
        if keys.add_key(self.resource.keytype, self.resource.key, self.resource.name):
            self.log.info("[%s] Added key to authorized_keys file %s" % (self, self.resource.path))
            keys.save(self.resource.path)
            self.resource.updated()
        else:
            self.log.debug("[%s] Key already in authorized_keys file %s" % (self, self.resource.path))

    def action_exclude(self):
        keys = SSHAuthorizedKeysFile(self.resource.path)
        if keys.remove_key(self.resource.keytype, self.resource.key):
            self.log.info("[%s] Removed key from authorized_keys file %s" % (self, self.resource.path))
            keys.save(self.resource.path)
            self.resource.updated()
        else:
            self.log.debug("[%s] Key not found in authorized_keys file %s" % (self, self.resource.path))
