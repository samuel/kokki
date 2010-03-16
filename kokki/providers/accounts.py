
from __future__ import with_statement

import grp
import os
import pwd
import subprocess
from kokki.base import Fail
from kokki.providers import Provider

class UserProvider(Provider):
    def action_create(self):
        user = self.user
        if user:
            pass
        else:
            pass

    @property
    def user(self):
        try:
            return pwd.getpwnam(self.resource.username)
        except KeyError:
            return None

    def create_user(self):
        ret = subprocess.check_call(cmd, shell=True, cwd=self.resource.cwd, env=self.resource.environment)

    def set_options(self):
        field_list = dict(
            comment = "-c",
            gid = "-g",
            uid = "-u",
            shell = "-s",
            password = "-p",
        )
