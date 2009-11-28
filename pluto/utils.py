
import pluto

class PlutoGlobals(dict):
    def __init__(self, *args, **kwargs):
        super(PlutoGlobals, self).__init__(*args, **kwargs)

        self.new_items = {}
        for k in dir(pluto):
            if not k.startswith('_'):
                self[k]= getattr(pluto, k)
        for name, obj in pluto.env.cookbooks.iteritems():
            self[name] = obj
        for name, obj in pluto.env.extra_resources.iteritems():
            self[name] = obj
        for name, obj in pluto.env.extra_providers.iteritems():
            self[name] = obj
        self.new_items = {}

    def __setitem__(self, name, value):
        self.new_items[name] = value
        super(PlutoGlobals, self).__setitem__(name, value)
