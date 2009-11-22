
__all__ = ["Fail", "Resource"]

import logging

class Fail(Exception):
    pass

class Resource(object):
    # Overriden by subclasses
    default_action = "nothing"
    actions = []
    attributes = {}

    # Global storage
    _resources = {}
    _changed = set()

    def __init__(self, name, action=None, ignore_failures=False, notifies=[], subscribers=[], not_if=None, only_if=None, **kwargs):
        self.name = name
        self.ignore_failures = ignore_failures
        self.notifies = notifies
        self.subscribers = subscribers
        self.not_if = not_if
        self.only_if = only_if

        self.log = logging.getLogger("pluto") #".resource.%s.%s" % (self.__class__.__name__, name))
        self.log.debug("New resource %s: %s" % (self, locals()))

        unknown_args = set(kwargs.keys()) - set(self.attributes.keys())
        if unknown_args:
            raise Fail("%s does not support the argument(s) %s" % (self.__class__.__name__, ",".join(unknown_args))) 

        for k, v in self.attributes.items():
            setattr(self, k, kwargs.get(k, v))

        if self.__class__ not in self._resources:
            self._resources[self.__class__] = {}
        self._resources[self.__class__][name] = self

        self.perform_action(action or self.default_action)

    def perform_action(self, action):
        if action != "nothing" and action not in self.actions:
            raise Fail("Trying to perform unsupported action '%s' on resource '%s'" % (action, self.__class__.__name__))
        self.log.debug("Performing action %s on %s" % (action, self))
        return getattr(self, action)()

    def nothing(self):
        pass

    def changed(self):
        self._changed.add(self)

    def __repr__(self):
        return "%s['%s']" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return u"%s['%s']" % (self.__class__.__name__, self.name)
