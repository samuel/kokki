
import pluto

class PlutoGlobals(dict):
    def __getitem__(self, name):
        try:
            return super(PlutoGlobals, self).__getitem__(name)
        except KeyError:
            pass

        try:
            return getattr(pluto, name)
        except AttributeError:
            pass

        try:
            return pluto.env.cookbooks[name]
        except KeyError:
            pass

        try:
            return pluto.env.extra_resources[name]
        except KeyError:
            pass

        try:
            return pluto.env.extra_providers[name]
        except KeyError:
            pass

        raise KeyError(name)
