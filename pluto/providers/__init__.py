
__all__ = ["find_provider"]

import logging
from pluto.environment import env

class Provider(object):
    def __init__(self, resource):
        self.log = logging.getLogger("pluto.provider")
        self.resource = resource

    def action_nothing(self):
        pass

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s[%s]" % (self.__class__.__name__, self.resource)

PROVIDERS = dict(
    debian = dict(
        Package = "pluto.providers.package.apt.DebianAptProvider",
        Service = "pluto.providers.service.debian.DebianServiceProvider",
    ),
    ubuntu = dict(
        Package = "pluto.providers.package.apt.DebianAptProvider",
        Service = "pluto.providers.service.debian.DebianServiceProvider",
    ),
    default = dict(
        File = "pluto.providers.system.FileProvider",
        Directory = "pluto.providers.system.DirectoryProvider",
        Link = "pluto.providers.system.LinkProvider",
        Execute = "pluto.providers.system.ExecuteProvider",
        Script = "pluto.providers.system.ScriptProvider",
    ),
)

def find_provider(resource, class_path=None):
    if not class_path:
        try:
            class_path = PROVIDERS[env.system.platform][resource]
        except KeyError:
            class_path = PROVIDERS["default"][resource]

    mod_path, class_name = class_path.rsplit('.', 1)
    mod = __import__(mod_path, {}, {}, [class_name])
    return getattr(mod, class_name)
