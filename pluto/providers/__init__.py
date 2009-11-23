
import logging
from pluto.environment import env

class Provider(object):
    def __init__(self, resource):
        self.log = logging.getLogger("pluto.provider")
        self.resource = resource

    def action_nothing(self):
        pass

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
        Execute = "pluto.providers.system.ExecuteProvider",
    ),
)

def find_provider(resource):
    try:
        class_path = PROVIDERS[env.system.platform][resource]
    except KeyError:
        class_path = PROVIDERS["default"][resource]

    mod_path, class_name = class_path.rsplit('.', 1)
    mod = __import__(mod_path, {}, {}, [class_name])
    return getattr(mod, class_name)
