
__all__ = ["File", "Directory", "Execute"]

import os
from pluto.base import *
from pluto.environment import env

class File(Resource):
    action = ResourceArgument(default="create")
    path = ResourceArgument()
    backup = ResourceArgument()
    mode = ResourceArgument()
    owner = ResourceArgument()
    group = ResourceArgument()
    content = ResourceArgument()

    def action_create(self):
        path = self.path or self.name
        write = False
        content = self._get_content()
        if not os.path.exists(path):
            write = True
        else:
            with open(path, "rb") as fp:
                if content != fp.read():
                    write = True

        if write:
            with open(path, "wb") as fp:
                if content:
                    fp.write(content)
            self.changed()

        if self.mode:
            st = os.stat(path)
            if (st.st_mode & 0777) != self.mode:
                os.chmod(path, self.mode)
                self.changed()

    def action_delete(self):
        path = self.path or self.name
        if os.path.exists(path):
            os.unlink(path)
            self.changed()

    def action_touch(self):
        path = self.path or self.name
        with open(path, "a") as fp:
            pass

    def _get_content(self):
        content = self.content
        if isinstance(content, basestring):
            return content
        elif hasattr(content, "__call__"):
            return content()
        raise Fail("Unknown source type for %s" % self)


class Directory(Resource):
    action = ResourceArgument(default="create")
    path = ResourceArgument()
    mode = ResourceArgument()
    owner = ResourceArgument()
    group = ResourceArgument()
    recursive = BooleanArgument(default=False)

    def action_create(self):
        path = self.path or self.name
        if not os.path.exists(path):
            if self.recursive:
                os.makedirs(path)
            else:
                os.makedir(path)
            self.changed()

        st = os.stat(path)
        if (st.st_mode & 0777) != self.mode:
            os.chmod(path, self.mode)
            self.changed()

    def action_delete(self):
        path = self.path or self.name
        if os.path.exists(path):
            os.rmdir(path)
            # TODO: recursive
            self.changed()

class Execute(Resource):
    action = ResourceArgument(default="run")
    command = ResourceArgument()
    creates = ResourceArgument()
    cwd = ResourceArgument()
    environment = ResourceArgument()
    user = ResourceArgument()
    group = ResourceArgument()
    returns = ResourceArgument(default=0)
    timeout = ResourceArgument()

    def action_run(self):
        if self.creates:
            if os.path.exists(self.creates):
                return

        ret = subprocess.call(self.command, cwd=self.cwd, env=self.environment)
        if ret != self.returns:
            raise Fail("%s failed, returned %d instead of %s" % (self, ret, self.returns))
        self.changed()
