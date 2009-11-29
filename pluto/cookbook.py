
from __future__ import with_statement

__all__ = ["register_cookbook_path", "load_cookbook"]

import imp
import os
import sys
import yaml

import pluto
from pluto.environment import env as global_env

class CookbookTemplate(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_metadata(self):
        if not hasattr(self, '_metadata'):
            path = os.path.join(self.path, "metadata.yaml")
            with open(path, "rb") as fp:
                self._metadata = yaml.load(fp.read())
        return self._metadata

    def get_default_attributes(self):
        meta = self.get_metadata()
        if 'attributes' in meta:
            return dict((k, v['default']) for k, v in meta['attributes'].items())
        return {}

    def get_recipe(self, name):
        path = os.path.join(self.path, "recipes", name + ".py")
        if not os.path.exists(path):
            return None

        with open(path, "rb") as fp:
            recipe = fp.read()

        return recipe

    def setup(self):
        pass

COOKBOOKS_MOD = "pluto.cookbooks"

class CookbookImporter(object):
    def __init__(self):
        self.cookbooks_module = imp.new_module("cookbooks")

    def find_module(self, fullname, path=None):
        if not fullname.startswith('pluto.cookbooks'):
            return None

        if fullname == COOKBOOKS_MOD:
            return self

        name = fullname[len(COOKBOOKS_MOD)+1:]

        return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        if fullname == COOKBOOKS_MOD:
            mod = self.cookbooks_module
            mod.__path__ = [fullname]
            mod.__file__ = "<%s>" % self.__class__.__name__
            sys.modules[fullname] = mod
        else:
            mod = None
            cb_name = fullname.split('.')[-1]
            for cp in cookbook_paths:
                cb_path = os.path.join(cp, cb_name, "__init__.py")
                if os.path.exists(cb_path):
                    mod = imp.new_module(fullname)
                    mod.__file__ = cb_path
                    mod.__path__ = ["%s/%s" % (COOKBOOKS_MOD.replace('.', '/'), cb_name)]
                    sys.modules[fullname] = mod
                    try:
                        execfile(cb_path, mod.__dict__)
                    except:
                        del sys.modules[fullname]
                        raise
            if not mod:
                return None

        mod.__loader__ = self
        mod.__package__ = "cookbooks"
        return mod

def load_cookbook(name, path=None, env=None):
    import imp
    import sys

    env = env or global_env

    try:
        return env.cookbooks[name]
    except KeyError:
        paths = [path] if path else sys.path
        for path in paths:
            cb_path = os.path.join(path, name)
            if os.path.exists(os.path.join(cb_path, 'metadata.yaml')):
                mod = __import__("pluto.cookbooks.%s" % name, {}, {}, [name])
                template = CookbookTemplate(name, cb_path)
                for k in dir(template):
                    if not hasattr(mod, k):
                        setattr(mod, k, getattr(template, k))
                env.cookbooks[name] = mod
                env.set_attributes(mod.get_default_attributes())
                globals()[name] = mod
                return mod

cookbook_paths = set()
importer = CookbookImporter()

def register_cookbook_path(path):
    cookbook_paths.add(path)
    # sys.path.append(path)

# @sys.path_hooks.append
# def cookbook_path_hook(path):
#     if path in cookbook_paths:
#         return importer
#     raise ImportError()

sys.meta_path.append(importer)
