
__all__ = ["File", "Directory", "Execute"]

import os
from pluto.base import *
from pluto.environment import env

class File(Resource):
    action = ResourceArgument(default="create")
    path = ResourceArgument(default=lambda obj:obj.name)
    backup = ResourceArgument()
    mode = ResourceArgument()
    owner = ResourceArgument()
    group = ResourceArgument()
    content = ResourceArgument()

    actions = ["create", "delete", "touch"]

class Directory(Resource):
    action = ResourceArgument(default="create")
    path = ResourceArgument(default=lambda obj:obj.name)
    mode = ResourceArgument()
    owner = ResourceArgument()
    group = ResourceArgument()
    recursive = BooleanArgument(default=False)

    actions = ["create", "delete"]

class Execute(Resource):
    action = ResourceArgument(default="run")
    command = ResourceArgument(default=lambda obj:obj.name)
    creates = ResourceArgument()
    cwd = ResourceArgument()
    environment = ResourceArgument()
    user = ResourceArgument()
    group = ResourceArgument()
    returns = ResourceArgument(default=0)
    timeout = ResourceArgument()

    actions = ["run"]
