
__all__ = ["SSHKnownHost", "SSHAuthorizedKey"]

import os.path
from kokki import *

class SSHKnownHost(Resource):
    provider = "*ssh.SSHKnownHostProvider"

    action = ForcedListArgument(default="include")
    host = ResourceArgument(default=lambda obj:obj.name)
    keytype = ResourceArgument()
    key = ResourceArgument()
    hashed = BooleanArgument(default=True)
    user = ResourceArgument()
    path = ResourceArgument()

    actions = Resource.actions + ["include", "exclude"]

    def validate(self):
        if not self.path:
            if not self.user:
                raise Fail("[%s] Either path or user is required" % self)
            self.path = os.path.join(ssh_path_for_user(self.user), "known_hosts")

class SSHAuthorizedKey(Resource):
    provider = "*ssh.SSHAuthorizedKeyProvider"

    action = ForcedListArgument(default="include")
    keytype = ResourceArgument()
    key = ResourceArgument()
    user = ResourceArgument()
    path = ResourceArgument()

    actions = Resource.actions + ["include", "exclude"]

    def validate(self):
        if not self.path:
            if not self.user:
                raise Fail("[%s] Either path or user is required" % self)
            self.path = os.path.join(ssh_path_for_user(self.user), "authorized_keys")
