
__all__ = ["include_recipe"]

import os
import pluto
from pluto.base import Fail
from pluto.cookbook import load_cookbook
from pluto.environment import env

def include_recipe(name):
    if name in env.included_recipes:
        return
    env.included_recipes.add(name)

    try:
        cookbook, recipe = name.split('.')
    except ValueError:
        cookbook, recipe = name, "default"

    cb = load_cookbook(cookbook)
    if not cb:
        raise Fail("Trying to include a recipe from an unknown cookbook %s" % name)

    rc = cb.get_recipe(recipe)
    globs = dict((k, getattr(pluto, k)) for k in dir(pluto))
    globs.update(env=env)
    exec rc in globs
