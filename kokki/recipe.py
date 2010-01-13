
__all__ = ["include_recipe"]

import os
import kokki
from kokki.base import Fail
from kokki.cookbook import load_cookbook
from kokki.environment import env

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

    globs = {}
    rc = cb.get_recipe(recipe)
    if not rc:
        raise Fail("Recipe %s in cookbook %s not found" % (recipe, cookbook))

    exec compile(rc, name, 'exec') in globs
