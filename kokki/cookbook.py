
from __future__ import with_statement

__all__ = ["register_cookbook_path", "load_cookbook"]

import imp
import os
import sys
import yaml

import kokki
from kokki.environment import env as global_env

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
        if meta.get('attributes'):
            return dict((k, v['default']) for k, v in meta['attributes'].items())
        else:
            meta['attributes'] = {}
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

COOKBOOKS_NAMESPACE = "kokki.cookbooks"

class CookbookImporter(object):
    def __init__(self):
        mod = self.cookbooks_module = imp.new_module("cookbooks")
        mod.__path__ = list(cookbook_paths)
        mod.__file__ = "<%s>" % self.__class__.__name__
        sys.modules[COOKBOOKS_NAMESPACE] = mod
        kokki.cookbooks = mod

    def find_module(self, fullname, path=None):
        if not fullname.startswith(COOKBOOKS_NAMESPACE):
            return None

        if self._find_module(fullname):
            return self

    def _find_module(self, fullname, path=None):
        mod_path = fullname[len(COOKBOOKS_NAMESPACE)+1:]
        current_name = "%s" % COOKBOOKS_NAMESPACE
        paths = path or list(cookbook_paths)
        for name in mod_path.split('.'):
            current_name += "."+name
            if current_name in sys.modules:
                paths = sys.modules[current_name].__path__
                continue

            return imp.find_module(name, paths)

    def _load_module(self, fullname, fp, pathname, description):
        if description[2] == 5:
            filename = os.path.join(pathname, "__init__.py")
            ispkg = True
        else:
            filename = pathname
            ispkg = False

        mod = imp.new_module(fullname)
        mod.__file__ = filename
        if ispkg:
            mod.__path__ = [pathname]
        sys.modules[fullname] = mod

        try:
            if fp:
                exec compile(fp.read(), filename, "exec") in mod.__dict__
            else:
                execfile(filename, mod.__dict__)
        except:
            del sys.modules[fullname]
            raise

        mod.__loader__ = self
        mod.__package__ = COOKBOOKS_NAMESPACE

        return mod

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        if fullname == COOKBOOKS_NAMESPACE:
            mod = self.cookbooks_module
            mod.__path__ = list(cookbook_paths)
            mod.__file__ = "<%s>" % self.__class__.__name__
            sys.modules[fullname] = mod
        else:
            fp, pathname, description = self._find_module(fullname)
            mod = self._load_module(fullname, fp, pathname, description)

            name = fullname[len(COOKBOOKS_NAMESPACE)+1:]
            if "." not in name:
                setattr(self.cookbooks_module, name, mod)

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
                parent_mod = __import__(COOKBOOKS_NAMESPACE, {}, {}, [name])
                mod = getattr(parent_mod, name)
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
