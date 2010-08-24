
__all__ = ["Provider", "find_provider"]

import logging
from kokki.base import Fail
from kokki.environment import env

class Provider(object):
    def __init__(self, resource):
        self.log = logging.getLogger("kokki.provider")
        self.resource = resource

    def action_nothing(self):
        pass

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s[%s]" % (self.__class__.__name__, self.resource)

PROVIDERS = dict(
    debian = dict(
        Package = "kokki.providers.package.apt.DebianAptProvider",
        Service = "kokki.providers.service.debian.DebianServiceProvider",
    ),
    ubuntu = dict(
        Package = "kokki.providers.package.apt.DebianAptProvider",
        Service = "kokki.providers.service.debian.DebianServiceProvider",
    ),
    default = dict(
        File = "kokki.providers.system.FileProvider",
        Directory = "kokki.providers.system.DirectoryProvider",
        Link = "kokki.providers.system.LinkProvider",
        Execute = "kokki.providers.system.ExecuteProvider",
        Script = "kokki.providers.system.ScriptProvider",
        Mount = "kokki.providers.mount.MountProvider",
        User = "kokki.providers.accounts.UserProvider",
        Group = "kokki.providers.accounts.GroupProvider",
    ),
)

def find_provider(resource, class_path=None):
    if not class_path:
        try:
            class_path = PROVIDERS[env.system.platform][resource]
        except KeyError:
            class_path = PROVIDERS["default"][resource]

    # elif '.' not in class_path:
    #     return env.extra_providers[class_path]

    try:
        mod_path, class_name = class_path.rsplit('.', 1)
    except ValueError:
        raise Fail("Unable to find provider for %s as %s" % (resource, class_path))
    mod = __import__(mod_path, {}, {}, [class_name])
    return getattr(mod, class_name)

