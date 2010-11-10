
__all__ = ["Kitchen", "Cookbook"]

import os
from kokki.environment import Environment
from kokki.exceptions import Fail
from kokki.system import System
from kokki.utils import AttributeDictionary

class Cookbook(object):
    def __init__(self, name, path, config=None):
        self.name = name
        self.path = path
        self._meta = None
        self._library = None

    @property
    def config(self):
        return self.meta.get('__config__', {})

    @property
    def loader(self):
        return self.meta.get('__loader__', lambda kit:None)

    @property
    def meta(self):
        if self._meta is None:
            metapath = os.path.join(self.path, "metadata.py")
            with open(metapath, "rb") as fp:
                source = fp.read()
            meta = {'system': System.get_instance()}
            exec compile(source, metapath, "exec") in meta
            self._meta = meta
        return self._meta

    @property
    def library(self):
        if self._library is None:
            libpath = os.path.join(self.path, "libraries")
            globs = {}

            if os.path.exists(libpath):
                for f in sorted(os.listdir(libpath)):
                    if not f.endswith('.py'):
                        continue

                    path = os.path.join(libpath, f)
                    with open(path, "rb") as fp:
                        source = fp.read()
                        exec compile(source, libpath, "exec") in globs
    
            self._library = AttributeDictionary(globs)
        return self._library

    def get_recipe(self, name):
        path = os.path.join(self.path, "recipes", name + ".py")
        if not os.path.exists(path):
            raise Fail("Recipe %s in cookbook %s not found" % (name, self.name))

        with open(path, "rb") as fp:
            return fp.read()

    def __getattr__(self, name):
        return self.library[name]

    @classmethod
    def load_from_path(cls, name, path):
        return cls(name, path)

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u"Cookbook['%s']" % self.name

class Kitchen(Environment):
    def __init__(self):
        super(Kitchen, self).__init__()
        self.included_recipes_order = [] 
        self.included_recipes = {}
        self.sourced_recipes = set()
        self.cookbooks = AttributeDictionary()
        self.cookbook_paths = []
        self.running = False

    def add_cookbook_path(self, *args):
        for path in args:
            # Check if it's a Python import path
            origpath = path
            if "." in path and not os.path.exists(path):
                pkg = __import__(path, {}, {}, path)
                path = os.path.dirname(os.path.abspath(pkg.__file__))
            self.cookbook_paths.append((origpath, os.path.abspath(path)))

    def register_cookbook(self, cb):
        self.update_config(dict((k, v.get('default')) for k, v in cb.config.items()), False)
        self.cookbooks[cb.name] = cb

    def load_cookbook(self, *args, **kwargs):
        for name in args:
            cb = None
            for origpath, path in reversed(self.cookbook_paths):
                fullpath = os.path.join(path, name)
                if not os.path.exists(fullpath):
                    continue
                cb = Cookbook.load_from_path(name, fullpath)

            if not cb:
                raise ImportError("Cookbook %s not found" % name)

            self.register_cookbook(cb)

    def include_recipe(self, *args):
        for name in args:
            if name in self.included_recipes:
                continue

            self.included_recipes_order.append(name)

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

            self.included_recipes[name] = (cb, recipe)

            if self.running:
                self.source_recipe(cb, recipe)

    def source_recipe(self, cookbook, recipe):
        name = "%s.%s" % (cookbook.name, recipe)
        if name in self.sourced_recipes:
            return

        self.sourced_recipes.add(name)
        cookbook.loader(self)

        rc = cookbook.get_recipe(recipe)
        globs = {'env': self}
        with self:
            exec compile(rc, name, 'exec') in globs

    def prerun(self):
        for name in self.included_recipes_order:
            cookbook, recipe = self.included_recipes[name]
            self.source_recipe(cookbook, recipe)

    def run(self):
        self.running = True
        self.prerun()
        super(Kitchen, self).run()
        self.running = False

    def __getstate__(self):
        state = super(Kitchen, self).__getstate__()
        state.update(
            cookbook_paths = [x[0] for x in self.cookbook_paths],
            included_recipes = self.included_recipes_order,
        )
        return state

    def __setstate__(self, state):
        super(Kitchen, self).__setstate__(state)
        for path in state['cookbook_paths']:
            self.add_cookbook_path(path)
        for recipe in state['included_recipes']:
            self.include_recipe(recipe)
