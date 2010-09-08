#!/usr/bin/env python

__all__ = ["Environment"]

import logging
from datetime import datetime
from functools import wraps
from subprocess import Popen, PIPE, STDOUT

from kokki.exceptions import Fail
from kokki.providers import find_provider
from kokki.version import long_version

def lazy_property(undecorated):
    name = '_' + undecorated.__name__
    @property
    @wraps(undecorated)
    def decorated(self):
        try:
            return getattr(self, name)
        except AttributeError:
            v = undecorated(self)
            setattr(self, name, v)
            return v
    return decorated

import os
import sys
class System(object):
    @lazy_property
    def os(self):
        platform = sys.platform
        if platform.startswith('linux'):
            return "linux"
        elif platform == "darwin":
            return "darwin"
        else:
            return "unknown"

    def unquote(self, val):
        if val[0] == '"':
            val = val[1:-1]
        return val

    @lazy_property
    def lsb(self):
        if os.path.exists("/etc/lsb-release"):
            with open("/etc/lsb-release", "rb") as fp:
                lsb = (x.split('=') for x in fp.read().strip().split('\n'))
            return dict((k.split('_', 1)[-1].lower(), self.unquote(v)) for k, v in lsb)
        elif os.path.exists("/usr/bin/lsb_release"):
            p = Popen(["/usr/bin/lsb_release","-a"], stdout=PIPE, stderr=PIPE)
            lsb = {}
            for l in p.communicate()[0].split('\n'):
                v = l.split(':', 1)
                if len(v) != 2:
                    continue
                lsb[v[0].strip().lower()] = self.unquote(v[1].strip().lower())
            lsb['id'] = lsb.pop('distributor id')
            return lsb

    @lazy_property
    def platform(self):
        operatingsystem = self.os
        if operatingsystem == "linux":
            lsb = self.lsb
            if not lsb:
                if os.path.exists("/etc/redhat-release"):
                    return "redhat"
                if os.path.exists("/etc/fedora-release"):
                    return "fedora"
                if os.path.exists("/etc/debian_version"):
                    return "debian"
            return lsb['id'].lower()
        elif operatingsystem == "darwin":
            out = Popen("/usr/bin/sw_vers", stdout=PIPE).communicate()[0]
            sw_vers = dict([y.strip() for y in x.split(':', 1)] for x in out.strip().split('\n'))
            # ProductName, ProductVersion, BuildVersion
            return sw_vers['ProductName'].lower().replace(' ', '_')
        else:
            return "unknown"

    @lazy_property
    def locales(self):
        p = Popen("locale -a", shell=True, stdout=PIPE)
        out = p.communicate()[0]
        return out.strip().split("\n")

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

class Environment(object):
    _instances = []

    def __init__(self):
        self.log = logging.getLogger("kokki")
        self.reset()

    def reset(self):
        self.system = System()
        self.config = AttributeDictionary()
        self.included_recipes = set()
        self.cookbooks = {}
        self.resources = {}
        self.resource_list = []
        self.delayed_actions = set()
        self.cookbook_paths = ["kokki.cookbooks"]
        self.update_config({'date': datetime.now(), 'kokki.long_version': long_version()})

    def update_config(self, attributes, overwrite=True):
        for k, v in attributes.items():
            attr = self.config
            path = k.split('.')
            for p in path[:-1]:
                if p not in attr:
                    attr[p] = AttributeDictionary()
                attr = attr[p]
            if overwrite or path[-1] not in attr:
                attr[path[-1]] = v

    def register_cookbook(self, name, mod):
        mod.__path__ = os.path.dirname(mod.__file__)
        self.update_config(dict((k, v.get('default')) for k, v in mod.__config__.items()), False)
        self.cookbooks[name] = mod

    def load_cookbook(self, *args, **kwargs):
        ignore_failed = kwargs.get('ignore_failed', False)
        for name in args:
            modname = name.rsplit('.')[-1]
            mod = None
            try:
                for n in ["%s.%s" % (x, name) for x in self.cookbook_paths] + [name]:
                    try:
                        with self:
                            mod = __import__(n, {}, {}, [modname])
                    except ImportError:
                        continue
                    else:
                        break
            except:
                if ignore_failed:
                    continue
                raise
            if not mod:
                raise ImportError("Cookbook %s not found" % name)

            if not hasattr(mod, '__description__') or not hasattr(mod, '__config__'):
                if not ignore_failed:
                    raise Fail("Invalid cookbook %s" % name)
                continue

            name = mod.__name__.rsplit('.', 1)[-1]
            self.register_cookbook(name, mod)

    def load_all_cookbooks(self, *args):
        for p in args:
            pkg = __import__(p, {}, {}, p)
            path = os.path.dirname(os.path.abspath(pkg.__file__))
            cookbooks = ["%s.%s" % (p, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            self.load_cookbook(*cookbooks, ignore_failed=True)

    def include_recipe(self, *args):
        for name in args:
            if name in self.included_recipes:
                continue

            self.included_recipes.add(name)

            try:
                cookbook, recipe = name.split('.')
            except ValueError:
                cookbook, recipe = name, "default"

            try:
                cb = self.cookbooks[cookbook]
            except KeyError:
                self.load_cookbook(cookbook)
                cb = self.cookbooks[cookbook]
                # raise Fail("Trying to include a recipe from an unknown cookbook %s" % name)

            globs = {'env': self}

            path = os.path.join(cb.__path__, "recipes", recipe + ".py")
            if not os.path.exists(path):
                raise Fail("Recipe %s in cookbook %s not found" % (recipe, cookbook))

            with open(path, "rb") as fp:
                rc = fp.read()

            with self:
                exec compile(rc, name, 'exec') in globs

    def run_action(self, resource, action):
        self.log.debug("Performing action %s on %s" % (action, resource))

        provider_class = find_provider(self, resource.__class__.__name__, resource.provider)
        provider = provider_class(resource)
        getattr(provider, 'action_%s' % action)()

        if resource.is_updated:
            for action, res in resource.subscriptions['immediate']:
                self.log.info("%s sending %s action to %s (immediate)" % (resource, action, res))
                self.run_action(res, action)
            for action, res in resource.subscriptions['delayed']:
                self.log.info("%s sending %s action to %s (delayed)" % (resource, action, res))
            self.delayed_actions |= resource.subscriptions['delayed']

    def _check_condition(self, cond):
        if hasattr(cond, '__call__'):
            return cond()

        if isinstance(cond, basestring):
            import subprocess
            ret = subprocess.call(cond, shell=True)
            return ret == 0

        raise Exception("Unknown condition type %r" % cond)

    def run(self):
        with self:
            # Run resource actions
            for resource in self.resource_list:
                if resource.not_if is not None and self._check_condition(resource.not_if):
                    self.log.debug("Skipping %s due to not_if" % resource)
                    continue

                if resource.only_if is not None and not self._check_condition(resource.only_if):
                    self.log.debug("Skipping %s due to only_if" % resource)
                    continue

                for action in resource.action:
                    self.run_action(resource, action)

            # Run delayed actions
            for action, resource in self.delayed_actions:
                self.run_action(resource, action)

    @classmethod
    def get_instance(cls):
        return cls._instances[-1]

    def __enter__(self):
        self.__class__._instances.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__class__._instances.pop()
        return False
