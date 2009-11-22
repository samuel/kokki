
__all__ = ["include_recipe"]

import os
from pluto.base import Fail
from pluto.environment import env

def include_recipe(name):
    if name in env.included_recipes:
        return

    try:
        cookbook, recipe = name.split('.')
    except ValueError:
        cookbook, recipe = name, "default"

    try:
        cb = env.cookbooks[cookbook]
    except KeyError:
        raise Fail("Trying to include a recipe from an unknown cookbook %s" % name)

    rc = cb.get_recipe(recipe)
    ret = eval(compile(rc, name, 'exec'))
    # path = os.path.join(env.path, cookbook, "recipes", recipe)
    # # ret = execfile(path, dict((k, getattr(pluto, k)) for k in dir(pluto) if not k.startswith('_')))
    # ret = execfile(path)
    env.included_recipes[recipe] = ret
