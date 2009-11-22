#!/usr/bin/env python

__all__ = ["Fail", "Resource", "ResourceArgument", "BooleanArgument"]

import logging

class Fail(Exception):
    pass

class InvalidArgument(Fail):
    pass

class ResourceArgument(object):
    def __init__(self, default=None, required=False):
        self.default = default
        self.required = required

    def validate(self, value):
        if self.required and value is None:
            raise InvalidArgument("Required argument %s missing" % self.name)
        return value

class BooleanArgument(ResourceArgument):
    def validate(self, value):
        value = super(BooleanArgument, self).validate(value)
        if not value in (True, False):
            raise InvalidArgument("Expected a boolean for %s received %r" % (self.name, value))

class Accessor(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls):
        try:
            return obj.arguments[self.name]
        except KeyError:
            return obj._arguments[self.name].default

    def __set__(self, obj, value):
        obj.arguments[self.name] = obj._arguments[self.name].validate(value)

class ResourceMetaclass(type):
    # def __new__(cls, name, bases, attrs):
    #     super_new = super(ResourceMetaclass, cls).__new__
    #     return super_new(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if name != "Resource":
            cls._resources[name] = {}
        cls._arguments = getattr(bases[0], '_arguments', {}).copy()
        for k, v in list(attrs.items()):
            if isinstance(v, ResourceArgument):
                v.name = k
                cls._arguments[k] = v
                setattr(cls, k, Accessor(k))#property(
                    # lambda self:self.arguments.get(k, self._arguments[k].default)))

class Resource(object):
    __metaclass__ = ResourceMetaclass

    _resources = {}
    _resource_list = []
    _changed = set()

    action = ResourceArgument(default="nothing")
    ignore_failures = BooleanArgument(default=False)
    notifies = ResourceArgument(default=[])
    subscribes = ResourceArgument(default=[])
    not_if = ResourceArgument()
    only_if = ResourceArgument()

    def __init__(self, name, **kwargs):
        self.name = name

        self.actions = {}
        for k in dir(self):
            if k.startswith('action_'):
                self.actions[k.split('_', 1)[1]] = getattr(self, k)

        self.arguments = {}
        for k, v in kwargs.items():
            try:
                arg = self._arguments[k]
            except KeyError:
                raise Fail("%s received unsupported argument %s" % (self, k))
            else:
                try:
                    self.arguments[k] = arg.validate(v)
                except InvalidArgument, exc:
                    raise InvalidArgument("%s %s" % (self, exc))

        self.log = logging.getLogger("pluto") #".resource.%s.%s" % (self.__class__.__name__, name))
        self.log.debug("New resource %s: %s" % (self, self.arguments))

        self._resources[self.__class__.__name__][name] = self
        self._resource_list.append(self)

        # self.perform_action(action or self.default_action)

    def lookup(self, resource_type, name):
        return self._resources[resource_type][name]

    def perform_action(self, action):
        if action not in self.actions:
            raise Fail("Trying to perform unsupported action '%s' on resource '%s'" % (action, self.__class__.__name__))
        self.log.debug("Performing action %s on %s" % (action, self))
        return self.actions[action]()

    def get_argument(self, key):
        try:
            return self.arguments[key]
        except KeyError:
            return self._arguments[key].default

    def action_nothing(self):
        pass

    def changed(self):
        self._changed.add(self)

    def __repr__(self):
        return "%s['%s']" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return u"%s['%s']" % (self.__class__.__name__, self.name)
