
from __future__ import with_statement

import grp
import os
import pwd
import subprocess
from kokki.base import Fail
from kokki.providers import Provider

class UserProvider(Provider):
    def action_create(self):
        if not self.user:
            command = ['useradd', self.resource.username]
            useradd_options = dict(
                comment = "-c",
                gid = "-g",
                uid = "-u",
                shell = "-s",
                password = "-p",
            )

            for option_name, option_value in self.resource.arguments.items():
                option_flag = useradd_options.get(option_name)
                if option_flag:
                    command += [option_flag, option_value]

            subprocess.check_call(command, shell=True, cwd=self.resource.cwd, env=self.resource.environment)
            self.resource.updated()

    @property
    def user(self):
        try:
            return pwd.getpwnam(self.resource.username)
        except KeyError:
            return None