
class AttributeDictionary(object):
    def __init__(self, *args, **kwargs):
        d = kwargs
        if args:
            d = args[0]
        super(AttributeDictionary, self).__setattr__("_dict", d)

    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        try:
            return self[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    def __setitem__(self, name, value):
        self._dict[name] = self._convert_value(value)

    def __getitem__(self, name):
        return self._convert_value(self._dict[name])

    def _convert_value(self, value):
        if isinstance(value, dict) and not isinstance(value, AttributeDictionary):
            return AttributeDictionary(value)
        return value

    def copy(self):
        return self.__class__(self._dict.copy())

    def items(self):
        return self._dict.items()

    def values(self):
        return self._dict.values()

    def keys(self):
        return self._dict.keys()

    def pop(self, *args, **kwargs):
        return self._dict.pop(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)

    def __repr__(self):
        return self._dict.__repr__()

    def __unicode__(self):
        return self._dict.__unicode__()

    def __str__(self):
        return self._dict.__str__()

    def __iter__(self):
        return self._dict.__iter__()
