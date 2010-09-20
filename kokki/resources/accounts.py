
__all__ = ["Group", "User"]

from kokki.base import *

class Group(Resource):
    action = ForcedListArgument(default="create")
    group_name = ResourceArgument(default=lambda obj:obj.name)
    gid = ResourceArgument()
    members = ForcedListArgument()
    password = ResourceArgument()
    # append = BooleanArgument(default=False) # NOT SUPPORTED

    actions = Resource.actions + ["create", "remove", "modify", "manage", "lock", "unlock"]

class User(Resource):
    action = ForcedListArgument(default="create")
    username = ResourceArgument(default=lambda obj:obj.name)
    comment = ResourceArgument()
    uid = ResourceArgument()
    gid = ResourceArgument()
    groups = ForcedListArgument() # supplementary groups
    home = ResourceArgument()
    shell = ResourceArgument(default="/bin/bash")
    password = ResourceArgument()
    system = BooleanArgument(default=False)

    actions = Resource.actions + ["create", "remove", "modify", "manage", "lock", "unlock"]
