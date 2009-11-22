
__all__ = ["File", "Directory", "Execute", "Template"]

import os
from pluto.base import Resource
from pluto.environment import env

class File(Resource):
    default_action = "create"
    actions = ["create", "delete", "touch"]
    attributes = dict(
        path = None,
        backup = False,
        mode = None,
        owner = None,
        group = None,
        content = None,
    )

    def create(self):
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

        st = os.stat(path)
        if (st.st_mode & 0777) != self.mode:
            os.chmod(path, self.mode)
            self.changed()

    def delete(self):
        path = self.path or self.name
        if os.path.exists(path):
            os.unlink(path)
            self.changed()

    def touch(self):
        path = self.path or self.name
        with open(path, "a") as fp:
            pass

    def _get_content(self):
        return self.content

class Template(File):
    attributes = dict(
        path = None,
        backup = False,
        mode = None,
        owner = None,
        group = None,
        source = None,
        variables = {},
    )

    def _get_content(self):
        from jinja2 import Environment, FileSystemLoader
        template_env = Environment(loader=FileSystemLoader(env.path), autoescape=False)
        template = template_env.get_template(self.source)
        context = self.variables.copy()
        context['env'] = env
        return template.render(context)

class Directory(Resource):
    default_action = "create"
    actions = ["create", "delete"]
    attributes = dict(
        path = None,
        mode = None,
        owner = None,
        group = None,
        recursive = False,
    )

    def create(self):
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

    def delete(self):
        path = self.path or self.name
        if os.path.exists(path):
            os.rmdir(path)
            # TODO: recursive
            self.changed()

class Execute(Resource):
    default_action = "run"
    actions = ["run"]
    attributes = dict(
        command = None,
        creates = None,
        cwd = None,
        environment = None,
        group = None,
        user = None,
        path = None,
        returns = 0,
        timeout = None,
    )

    def run(self):
        if self.creates:
            if os.path.exists(self.creates):
                return

        ret = subprocess.call(self.command, cwd=self.cwd, env=self.environment)
        if ret != self.returns:
            raise Fail("%s failed, returned %d instead of %s" % (self, ret, self.returns))
        self.changed()
