#!/usr/bin/env python

__all__ = ["Fail", "Resource", "ResourceArgument", "ForcedListArgument", "BooleanArgument"]

import logging
from kokki.environment import env as global_env

class Fail(Exception):
    pass

class InvalidArgument(Fail):
    pass

class ResourceArgument(object):
    def __init__(self, default=None, required=False, allow_override=False):
        self.required = False # Prevents the initial validate from failing
        self.default = self.validate(default)
        self.required = required
        self.allow_override = allow_override

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
        return value

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
        cls._arguments = getattr(bases[0], '_arguments', {}).copy()
        for k, v in list(attrs.items()):
            if isinstance(v, ResourceArgument):
                v.name = k
                cls._arguments[k] = v
                setattr(cls, k, Accessor(k))#property(
                    # lambda self:self.arguments.get(k, self._arguments[k].default)))

class Resource(object):
    __metaclass__ = ResourceMetaclass

    is_updated = False

    action = ForcedListArgument(default="nothing")
    ignore_failures = BooleanArgument(default=False)
    notifies = ResourceArgument(default=[])
    subscribes = ResourceArgument(default=[])
    not_if = ResourceArgument()
    only_if = ResourceArgument()

    actions = ["nothing"]

    def __new__(cls, name, env=None, provider=None, **kwargs):
        env = env or global_env
        provider = provider or getattr(cls, 'provider', None)

        r_type = cls.__name__
        if r_type not in env.resources:
            env.resources[r_type] = {}
        if name not in env.resources[r_type]:
            obj = super(Resource, cls).__new__(cls)
            env.resources[r_type][name] = obj
            env.resource_list.append(obj)
            return obj

        obj = env.resources[r_type][name]
        if obj.provider != provider:
            raise Fail("Duplicate resource %r with a different provider %r != %r" % (obj, provider, obj.provider))

        obj.override(**kwargs)
        return obj

    def __init__(self, name, env=None, provider=None, **kwargs):
        if hasattr(self, 'name'):
            return

        self.name = name
        self.env = env or global_env
        self.provider = provider or getattr(self, 'provider', None)
        self.log = logging.getLogger("kokki.resoruce")

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

        self.log.debug("New resource %s: %s" % (self, self.arguments))
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

        self.validate()

    def validate(self):
        pass

    def subscribe(self, action, resource, immediate=False):
        imm = "immediate" if immediate else "delayed"
        sub = (action, resource)
        self.subscriptions[imm].add(sub)

    def updated(self):
        self.is_updated = True

    def override(self, **kwargs):
        for k, v in kwargs.items():
            try:
                arg = self._arguments[k]
            except KeyError:
                raise Fail("%s received unsupported argument %s" % (self, k))
            else:
                if v != self.arguments.get(k):
                    if not arg.allow_override:
                        raise Fail("%s doesn't allow overriding argument '%s'" % (self, k))

                    try:
                        self.arguments[k] = arg.validate(v)
                    except InvalidArgument, exc:
                        raise InvalidArgument("%s %s" % (self, exc))
        self.validate()

    def __repr__(self):
        return "%s['%s']" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return u"%s['%s']" % (self.__class__.__name__, self.name)
