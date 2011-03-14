
__all__ = ["RedhatServiceProvider"]

from kokki.providers.service import ServiceProvider

class RedhatServiceProvider(ServiceProvider):
    def enable_runlevel(self, runlevel):
        pass
