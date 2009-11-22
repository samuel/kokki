
__all__ = ["load_cookbook"]

import os
import yaml
from pluto.environment import env

class Cookbook(object):
    def __init__(self, path):
        path = os.path.abspath(path)
        if path[-1] == '/':
            path = path[:-1]

        self.path = path
        self.name = path.rsplit('/', 1)[-1]
        self.loaded = False

    def load(self):
        if self.loaded:
            return

        meta = self.get_metadata()
        env.load_attributes(dict((k, v['default']) for k, v in meta['attributes'].items()))

        self.mod = __import__(self.name, {}, {}, [self.name])
        self.mod.setup_environment()

    def get_recipe(self, name):
        self.load()
        name = name + ".py"
        path = os.path.join(self.path, "recipes", name)
        with open(path, "rb") as fp:
            recipe = fp.read()
        return recipe

    def get_metadata(self):
        if not hasattr(self, '_metadata'):
            path = os.path.join(self.path, "metadata.yaml")
            with open(path, "rb") as fp:
                self._metadata = yaml.load(fp.read())
        return self._metadata

def load_cookbook(name):
    env.cookbooks[name] = Cookbook(os.path.join(env.path, name))
