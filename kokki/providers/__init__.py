
__all__ = ["Provider", "find_provider"]

import logging
from kokki.exceptions import Fail

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
    redhat = dict(
        Service = "kokki.providers.service.redhat.RedhatServiceProvider",
        Package = "kokki.providers.package.yumrpm.YumProvider",
    ),
    centos = dict(
        Service = "kokki.providers.service.redhat.RedhatServiceProvider",
        Package = "kokki.providers.package.yumrpm.YumProvider",
    ),
    fedora = dict(
        Service = "kokki.providers.service.redhat.RedhatServiceProvider",
        Package = "kokki.providers.package.yumrpm.YumProvider",
    ),
    gentoo = dict(
        Package = "kokki.providers.package.emerge.GentooEmergeProvider",
        Service = "kokki.providers.service.gentoo.GentooServiceProvider",
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

def find_provider(env, resource, class_path=None):
    if not class_path:
        try:
            class_path = PROVIDERS[env.system.platform][resource]
        except KeyError:
            class_path = PROVIDERS["default"][resource]

    if class_path.startswith('*'):
        cookbook, classname = class_path[1:].split('.')
        return getattr(env.cookbooks[cookbook], classname)

    try:
        mod_path, class_name = class_path.rsplit('.', 1)
    except ValueError:
        raise Fail("Unable to find provider for %s as %s" % (resource, class_path))
    mod = __import__(mod_path, {}, {}, [class_name])
    return getattr(mod, class_name)
