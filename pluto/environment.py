#!/usr/bin/env python

from __future__ import with_statement

__all__ = ["env"]

from functools import wraps
from subprocess import Popen, PIPE, STDOUT

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
        else:
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
        os = self.os
        if os == "linux":
            lsb = self.lsb
            return lsb['id'].lower()
        elif os == "darwin":
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

class Environment(AttributeDictionary):
    system = System()

    def __init__(self):
        self.reset()

    def reset(self):
        self.clear()
        self.included_recipes = set()
        self.cookbooks = {}
        self.resources = {}
        self.resource_list = []

    def set_attributes(self, attributes, overwrite=False):
        for k, v in attributes.items():
            attr = self
            path = k.split('.')
            for p in path[:-1]:
                if p not in attr:
                    attr[p] = AttributeDictionary()
                attr = attr[p]
            if overwrite or path[-1] not in attr:
                attr[path[-1]] = v

env = Environment()
