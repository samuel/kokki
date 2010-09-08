
from __future__ import with_statement

__all__ = ["Source", "Template", "StaticFile"]

import os
from kokki import environment

class Source(object):
    def get_content(self):
        raise NotImplementedError()

    def get_checksum(self):
        return None

    def __call__(self):
        return self.get_content()

class StaticFile(Source):
    def __init__(self, name, env=None):
        self.name = name
        self.env = env or environment.Environment.get_instance()

    def get_content(self):
        cookbook, name = self.name.split('/', 1)
        cb = self.env.cookbooks[cookbook]
        path = os.path.join(cb.__path__, "files", name)
        with open(path, "rb") as fp:
            return fp.read()

try:
    from jinja2 import Environment, BaseLoader, TemplateNotFound
except ImportError:
    class Template(Source):
        def __init__(self, name, variables=None, env=None):
            raise Exception("Jinja2 required for Template")
else:
    class TemplateLoader(BaseLoader):
        def __init__(self, env=None):
            self.env = env or environment.Environment.get_instance()

        def get_source(self, environment, template):
            cookbook, name = template.split('/', 1)
            cb = self.env.cookbooks[cookbook]
            path = os.path.join(cb.__path__, "templates", name)
            if not os.path.exists(path):
                raise TemplateNotFound(template)
            mtime = os.path.getmtime(path)
            with open(path, "rb") as fp:
                source = fp.read().decode('utf-8')
            return source, path, lambda:mtime == os.path.getmtime(path)

    class Template(Source):
        def __init__(self, name, variables=None, env=None):
            self.name = name
            self.env = env or environment.Environment.get_instance()
            self.context = variables.copy() if variables else {}
            self.template_env = Environment(loader=TemplateLoader(self.env), autoescape=False)
            self.template = self.template_env.get_template(self.name)

        def get_content(self):
            self.context.update(
                env = self.env,
                repr = repr,
                str = str,
                bool = bool,
            )
            rendered = self.template.render(self.context)
            return rendered + "\n" if not rendered.endswith('\n') else rendered
