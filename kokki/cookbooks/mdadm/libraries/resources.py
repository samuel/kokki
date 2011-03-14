
from kokki import Resource, ForcedListArgument, ResourceArgument

class Array(Resource):
    provider = "*mdadm.ArrayProvider"

    actions = Resource.actions + ["create", "stop", "assemble"]

    action = ForcedListArgument(default="create")
    chunksize = ResourceArgument()
    level = ResourceArgument()
    metadata = ResourceArgument()
    devices = ForcedListArgument()

    def __init__(self, *args, **kwargs):
        super(Array, self).__init__(*args, **kwargs)
        self.subscribe("run", self.env.resources["Execute"]["mdadm-update-conf"], False)
