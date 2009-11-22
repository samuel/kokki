
__all__ = ["include_recipe"]

import os
import pluto
from pluto.environment import env

def include_recipe(recipe):
    if recipe in env.included_recipes:
        return

    try:
        cookbook, recipe = recipe.split('.')
        recipe = recipe + ".py"
    except ValueError:
        cookbook, recipe = recipe, "default.py"
    path = os.path.join(env.path, cookbook, "recipes", recipe)
    ret = execfile(path, dict((k, getattr(pluto, k)) for k in dir(pluto) if not k.startswith('_')))
    # with open(path, "rb") as fp:
    #     source = fp.read()
    #     source = "from pluto import *\n" + source
    #     print source
    #     ret = eval(source)
    env.included_recipes[recipe] = ret
