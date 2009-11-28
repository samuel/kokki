
from __future__ import with_statement

__all__ = ["CookbookBase", "load_cookbook"]

import os
import yaml
import pluto
from pluto.environment import env as global_env
from pluto.utils import PlutoGlobals

class CookbookBase(object):
    def __init__(self, name=None, path=None, env=None):
        if not path:
            path = os.path.dirname(self.__class__.__file__)

        path = os.path.abspath(path)
        if path[-1] == '/':
            path = path[:-1]

        self.path = path
        self.name = name or path.rsplit('/', 1)[-1]
        self.providers = self.load_classes("providers", pluto.Provider)
        self.resources = self.load_classes("resources", pluto.Resource)
        self.definitions = self.load_definitions()

    def get_default_attributes(self):
        meta = self.metadata
        if 'attributes' in meta:
            return dict((k, v['default']) for k, v in meta['attributes'].items())
        return {}

    def override_attributes(self, env):
        a_path = os.path.join(self.path, "environment.py")
        if os.path.exists(a_path):
            globs = PlutoGlobals()
            execfile(a_path, globs)

    def load_classes(self, name, ancestor):
        source_path = os.path.join(self.path, name)
        classes = {}
        if os.path.exists(source_path):
            for rfile in os.listdir(source_path):
                a_path = os.path.join(source_path, rfile)
                globs = PlutoGlobals()
                execfile(a_path, globs)
                for k, v in globs.new_items.items():
                    if not k.startswith('_') and isinstance(v, type) and issubclass(v, ancestor):
                        classes[k] = v
        return classes

    def load_definitions(self):
        source_path = os.path.join(self.path, "definitions")
        defs = {}
        if os.path.exists(source_path):
            for rfile in os.listdir(source_path):
                a_path = os.path.join(source_path, rfile)
                globs = PlutoGlobals()
                execfile(a_path, globs)
                for k, v in globs.new_items.items():
                    if not k.startswith('_') and hasattr(v, '__call__'):
                        defs[k] = v
        return defs

    def get_recipe(self, name):
        path = os.path.join(self.path, "recipes", name + ".py")
        if not os.path.exists(path):
            return None

        with open(path, "rb") as fp:
            recipe = fp.read()

        return recipe

    @property
    def metadata(self):
        if not hasattr(self, '_metadata'):
            path = os.path.join(self.path, "metadata.yaml")
            with open(path, "rb") as fp:
                self._metadata = yaml.load(fp.read())
        return self._metadata

    def __getattr__(self, name):
        try:
            return self.providers[name]
        except KeyError:
            pass
        try:
            return self.resources[name]
        except KeyError:
            pass
        try:
            return self.definitions[name]
        except KeyError:
            pass
        raise AttributeError("Cookbook %s does not have attribute %s" % (self.name, name))

def load_cookbook(name, path=None, env=None):
    import sys

    env = env or global_env

    try:
        return env.cookbooks[name]
    except KeyError:
        paths = [path] if path else sys.path
        for path in paths:
            cb_path = os.path.join(path, name)
            if os.path.exists(os.path.join(cb_path, 'metadata.yaml')):
                cb = CookbookBase(name, cb_path, env)
                env.cookbooks[name] = cb
                env.set_attributes(cb.get_default_attributes())
                cb.override_attributes(env)
                env.extra_providers.update(cb.providers)
                env.extra_resources.update(cb.resources)
                return cb
