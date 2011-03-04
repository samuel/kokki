
__all__ = ["Package"]

import subprocess
from kokki.base import *

class Package(Resource):
    action = ForcedListArgument(default="install")
    package_name = ResourceArgument(default=lambda obj:obj.name)
    location = ResourceArgument(default=lambda obj:obj.package_name)
    version = ResourceArgument()
    actions = ["install", "upgrade", "remove", "purge"]