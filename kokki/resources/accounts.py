
__all__ = ["Group", "User"]

from kokki.base import *
from kokki.environment import env

class Group(Resource):
    action = ForcedListArgument(default="create")
    group_name = ResourceArgument(default=lambda obj:obj.name)
    gid = ResourceArgument()
    members = ForcedListArgument()
    home = ResourceArgument()
    append = BooleanArgument(default=False)

    actions = Resource.actions + ["create", "remove", "Modify", "manage", "lock", "unlock"]

class User(Resource):
    action = ForcedListArgument(default="create")
    username = ResourceArgument(default=lambda obj:obj.name)
    comment = ResourceArgument()
    uid = ResourceArgument()
    gid = ResourceArgument()
    home = ResourceArgument()
    shell = ResourceArgument()
    password = ResourceArgument()

    actions = Resource.actions + ["create", "remove", "Modify", "manage", "lock", "unlock"]
