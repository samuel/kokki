
__all__ = ["CookbookBase", "load_cookbook"]

import os
import yaml
from pluto.environment import env as global_env

class CookbookBase(object):
    def __init__(self, name=None, path=None, env=None):
        if not path:
            path = os.path.dirname(self.__class__.__file__)

        path = os.path.abspath(path)
        if path[-1] == '/':
            path = path[:-1]

        self.path = path
        self.name = name or path.rsplit('/', 1)[-1]
        self.env = env or global_env
        self.setup_environment()

    def setup_environment(self):
        meta = self.metadata
        if 'attributes' in meta:
            self.env.set_attributes(dict((k, v['default']) for k, v in meta['attributes'].items()))

        a_path = os.path.join(self.path, "environment.py")
        if os.path.exists(a_path):
            with open(a_path, "rb") as fp:
                code = fp.read()
                exec code in {'env':self.env}

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

def load_cookbook(name, env=None):
    import sys

    env = env or global_env

    try:
        return env.cookbooks[name]
    except KeyError:
        for path in sys.path:
            cb_path = os.path.join(path, name)
            if os.path.exists(os.path.join(cb_path, 'metadata.yaml')):
                cb = CookbookBase(name, cb_path, env)
                env.cookbooks[name] = cb
                return cb
