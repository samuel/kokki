
__all__ = ["GentooServiceProvider"]

from kokki.providers.service import ServiceProvider

class GentooServiceProvider(ServiceProvider):
    def enable_runlevel(self, runlevel):
        pass
