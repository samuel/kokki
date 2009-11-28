
from __future__ import with_statement

__all__ = ["load_cookbook"]

import os
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
                init_path = os.path.join(cb_path, "__init__.py")
                with open(init_path, "rb") as fp:
                    mod = imp.load_module("pluto.cookbook.%s" % name, fp, init_path, ('.py', 'U', 1))
                template = CookbookTemplate(name, cb_path)
                for k in dir(template):
                    if not hasattr(mod, k):
                        setattr(mod, k, getattr(template, k))
                env.cookbooks[name] = mod
                env.set_attributes(mod.get_default_attributes())
                mod.setup()
                globals()[name] = mod
                # cb = CookbookBase(name, cb_path, env)
                # env.cookbooks[name] = cb
                # env.set_attributes(cb.get_default_attributes())
                # cb.override_attributes(env)
                # env.extra_providers.update(cb.providers)
                # env.extra_resources.update(cb.resources)
                # env.extra_definitions.update(cb.definitions)
                return mod
