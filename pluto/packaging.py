
__all__ = ["Package"]

import subprocess
from pluto.base import *

class Package(Resource):
    action = ResourceArgument(default="install")
    package_name = ResourceArgument(default=lambda obj:obj.name)
    version = ResourceArgument()
    actions = ["install", "upgrade", "remove", "purge"]
