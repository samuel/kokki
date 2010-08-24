import subprocess

from kokki.base import Fail
from kokki.providers import Provider
from kokki.providers.service import ServiceProvider

class RedhatServiceProvider(ServiceProvider):
    def enable_runlevel(self, runlevel):
        pass
