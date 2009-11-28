
__all__ = ["include_recipe"]

import os
import pluto
from pluto.base import Fail
from pluto.cookbook import load_cookbook
from pluto.environment import env
from pluto.utils import PlutoGlobals

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

    globs = PlutoGlobals()
    rc = cb.get_recipe(recipe)
    exec compile(rc, name, 'exec') in globs
