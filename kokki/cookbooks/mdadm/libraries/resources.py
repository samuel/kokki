
from kokki import *

class Array(Resource):
    provider = "*mdadm.ArrayProvider"

    actions = Resource.actions + ["create", "stop"]

    action = ForcedListArgument(default="create")
    chunksize = ResourceArgument()
    level = ResourceArgument()
    metadata = ResourceArgument()
    devices = ForcedListArgument()
