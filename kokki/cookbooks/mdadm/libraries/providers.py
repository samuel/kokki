
import os
import subprocess
import time
from kokki import *

class ArrayProvider(Provider):
    def action_create(self):
        if not self.exists():
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
        if self.exists():
            subprocess.check_call(["/sbin/mdadm",
                    "--stop", self.resource.name])
            self.wait_for_array(False)
            self.resource.updated()

    def action_assemble(self):
        if not self.exists():
            subprocess.check_call(["/sbin/mdadm",
                    "--assemble", self.resource.name,
                ] + self.resource.devices)
            self.wait_for_array(True)
            self.resource.updated()

    def exists(self):
        ret = subprocess.call(["/sbin/mdadm", "-Q", self.resource.name])
        return not ret

    def wait_for_array(self, exists):
        for i in range(10):
            if exists == self.exists():
                break
            time.sleep(0.5)
