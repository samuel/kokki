
import os
import subprocess
from kokki import *

class ArrayProvider(Provider):
    def action_create(self):
        if not os.path.exists(self.resource.name):
            subprocess.check_call(["/sbin/mdadm",
                    "--create", self.resource.name,
                    "-R",
                    "-c", str(self.resource.chunksize),
                    "--level", str(self.resource.level),
                    "--metadata", self.resource.metadata,
                    "--raid-devices", len(self.resource.devices),
                ] + self.resource.devices)
            self.resource.updated()
