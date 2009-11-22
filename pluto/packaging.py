
__all__ = ["Package"]

import subprocess
from pluto.base import *
from pluto.providers.package.apt import DebianAPTProvider

class Package(Resource):
    package_name = ResourceArgument()
    version = ResourceArgument()
    actions = ["install", "upgrade", "remove", "purge"]
