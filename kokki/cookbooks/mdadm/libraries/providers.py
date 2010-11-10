
import os
import subprocess
import time
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
                    "--raid-devices", str(len(self.resource.devices)),
                ] + self.resource.devices)
            self.wait_for_array(True)
            self.resource.updated()
    
    def action_stop(self):
        if os.path.exists(self.resource.name):
            subprocess.check_call(["/sbin/mdadm",
                    "--stop", self.resource.name])
            self.wait_for_array(False)
            self.resource.updated()

    def action_assemble(self):
        if not os.path.exists(self.resource.name):
            subprocess.check_call(["/sbin/mdadm",
                    "--assemble", self.resource.name,
                ] + self.resource.devices)
            self.wait_for_array(True)
            self.resource.updated()

    def wait_for_array(self, exists):
        for i in range(10):
            if exists == os.path.exists(self.resource.name):
                break
            time.sleep(0.5)
