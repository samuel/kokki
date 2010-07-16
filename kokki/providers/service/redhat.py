import subprocess

from kokki.base import Fail
from kokki.providers import Provider

class RedhatServiceProvider(ServiceProvider):
    def enable_runlevel(self,runlevel):
        pass
