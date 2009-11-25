
__all__ = ["File", "Directory", "Link", "Execute", "Script"]

import os
from pluto.base import *
from pluto.environment import env

class File(Resource):
    action = ForcedListArgument(default="create")
    path = ResourceArgument(default=lambda obj:obj.name)
    backup = ResourceArgument()
    mode = ResourceArgument()
    owner = ResourceArgument()
    group = ResourceArgument()
    content = ResourceArgument()

    actions = Resource.actions + ["create", "delete", "touch"]

class Directory(Resource):
    action = ForcedListArgument(default="create")
    path = ResourceArgument(default=lambda obj:obj.name)
    mode = ResourceArgument()
    owner = ResourceArgument()
    group = ResourceArgument()
    recursive = BooleanArgument(default=False)

    actions = Resource.actions + ["create", "delete"]

class Link(Resource):
    action = ForcedListArgument(default="create")
    path = ResourceArgument(default=lambda obj:obj.name)
    to = ResourceArgument(required=True)
    hard = BooleanArgument(default=False)

    actions = Resource.actions + ["create", "delete"]

class Execute(Resource):
    action = ForcedListArgument(default="run")
    command = ResourceArgument(default=lambda obj:obj.name)
    creates = ResourceArgument()
    cwd = ResourceArgument()
    environment = ResourceArgument()
    user = ResourceArgument()
    group = ResourceArgument()
    returns = ResourceArgument(default=0)
    timeout = ResourceArgument()

    actions = Resource.actions + ["run"]

class Script(Resource):
    action = ForcedListArgument(default="run")
    code = ResourceArgument(required=True)
    interpreter = ResourceArgument(default="/bin/bash")

    action = Resource.actions + ["run"]
