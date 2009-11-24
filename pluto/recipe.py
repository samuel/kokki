
__all__ = ["include_recipe"]

import os
from pluto.base import Fail
from pluto.environment import env

def include_recipe(name):
    if name in env.included_recipes:
        return
    env.included_recipes.add(name)

    try:
        cookbook, recipe = name.split('.')
    except ValueError:
        cookbook, recipe = name, "default"

    # name = "%s.recipes%s" % (cookbook, "."+recipe if recipe else "")

    try:
        cb = env.cookbooks[cookbook]
    except KeyError:
        raise Fail("Trying to include a recipe from an unknown cookbook %s" % name)
    
    rc = cb.get_recipe(recipe)
    eval(compile(rc, name, 'exec'))

    # mod = __import__(name, {}, {}, [name])
