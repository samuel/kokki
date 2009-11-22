#!/usr/bin/env python

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

class System(object):
    @lazy_property
    def os(self):
        import sys
        platform = sys.platform
        if platform.startswith('linux'):
            return "linux"
        elif platform == "darwin":
            return "darwin"
        else:
            return "unknown"

    @lazy_property
    def lsb(self):
        return dict(x.split('=') for x in open("/etc/lsb-release", "rb").read().strip().split('\n'))

    @lazy_property
    def platform(self):
        os = self.os
        if os == "linux":
            lsb = self.lsb
            return lsb['DISTRIB_ID'].lower()
        elif os == "darwin":
            out = Popen("/usr/bin/sw_vers", stdout=PIPE).communicate()[0]
            sw_vers = dict([y.strip() for y in x.split(':', 1)] for x in out.strip().split('\n'))
            # ProductName, ProductVersion, BuildVersion
            return sw_vers['ProductName'].lower().replace(' ', '_')
        else:
            return "unknown"

class Environment(dict):
    system = System()

    def __init__(self):
        self.attr = {}
        self.path = None
        self.included_recipes = {}
        self.cookbooks = {}

    def load_attributes(self, attributes):
        for k, v in attributes.items():
            attr = self.attr
            path = k.split('.')
            for p in path[:-1]:
                if p not in attr:
                    attr[p] = {}
                attr = attr[p]
            attr[path[-1]] = v

env = Environment()
