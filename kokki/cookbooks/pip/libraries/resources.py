
__all__ = ["PipPackage"]

import os.path
from kokki import *


class PipPackage(Resource):
    provider = "*pip.PipPackageProvider"

    action = ForcedListArgument(default="install")
    package_name = ResourceArgument(default=lambda obj:obj.name)
    location = ResourceArgument(default=lambda obj:obj.package_name)
    version = ResourceArgument(required = True)
    actions = ["install", "upgrade", "remove", "purge"]