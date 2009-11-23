#!/usr/bin/env python

__all__ = ["Fail", "Resource", "ResourceArgument", "ForcedListArgument", "BooleanArgument"]

import logging
from pluto.providers import find_provider
from pluto.environment import env as global_env

class Fail(Exception):
    pass

class InvalidArgument(Fail):
    pass

class ResourceArgument(object):
    def __init__(self, default=None, required=False):
        self.required = required
        self.default = self.validate(default)

    def validate(self, value):
        if self.required and value is None:
            raise InvalidArgument("Required argument %s missing" % self.name)
        return value

class ForcedListArgument(ResourceArgument):
    def validate(self, value):
        value = super(ForcedListArgument, self).validate(value)
        if isinstance(value, basestring):
            value = [value]
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
            val = obj._arguments[self.name].default
            if hasattr(val, '__call__'):
                val = val(obj)
            return val

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

    is_updated = False

    action = ForcedListArgument(default="nothing")
    ignore_failures = BooleanArgument(default=False)
    notifies = ResourceArgument(default=[])
    subscribes = ResourceArgument(default=[])
    not_if = ResourceArgument()
    only_if = ResourceArgument()

    actions = ["nothing"]

    def __init__(self, name, env=None, provider=None, **kwargs):
        self.name = name
        self.env = env or global_env
        self.provider = provider

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

        self.log = logging.getLogger("pluto.resoruce")
        self.log.debug("New resource %s: %s" % (self, self.arguments))

        self._resources[self.__class__.__name__][name] = self
        self._resource_list.append(self)

        self.subscriptions = {'immediate': set(), 'delayed': set()}

        for sub in self.subscribes:
            if len(sub) == 2:
                action, res = sub
                immediate = False
            else:
                action, res, immediate = sub

            res.subscribe(action, self, immediate)

        for sub in self.notifies:
            self.subscribe(*sub)

    @classmethod
    def lookup(cls, resource_type, name):
        return cls._resources[resource_type][name]

    def subscribe(self, action, resource, immediate=False):
        imm = "immediate" if immediate else "delayed"
        sub = (action, resource)
        self.subscriptions[imm].add(sub)

    def updated(self):
        self.is_updated = True

    def __repr__(self):
        return "%s['%s']" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return u"%s['%s']" % (self.__class__.__name__, self.name)
