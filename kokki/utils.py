
class AttributeDictionary(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    def __setitem__(self, name, value):
        super(AttributeDictionary, self).__setitem__(name, self._convert_value(value))

    def __getitem__(self, name):
        return self._convert_value(super(AttributeDictionary, self).__getitem__(name))

    def _convert_value(self, value):
        if isinstance(value, dict) and not isinstance(value, AttributeDictionary):
            return AttributeDictionary(value)
        return value
