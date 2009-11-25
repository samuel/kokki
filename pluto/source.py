
__all__ = ["Source", "Template"]

import os
from jinja2 import Environment, BaseLoader, TemplateNotFound
from pluto.environment import env as global_env

class Source(object):
    def get_content(self):
        raise NotImplementedError()

    def get_checksum(self):
        return None

class TemplateLoader(BaseLoader):
    def __init__(self, env=None):
        self.env = env or global_env

    def get_source(self, environment, template):
        cookbook, name = template.split('/', 1)
        cb = self.env.cookbooks[cookbook]
        path = os.path.join(cb.path, "templates", name)
        if not os.path.exists(path):
            raise TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path, "rb") as fp:
            source = fp.read().decode('utf-8')
        return source, path, lambda:mtime == os.path.getmtime(path)

class Template(Source):
    def __init__(self, name, variables=None, env=None):
        self.name = name
        self.env = env or global_env
        self.context = variables.copy() if variables else {}
        self.template_env = Environment(loader=TemplateLoader(self.env), autoescape=False)
        self.template = self.template_env.get_template(self.name)

    def get_content(self):
        self.context['env'] = self.env
        rendered = self.template.render(self.context)
        return rendered + "\n" if not rendered.endswith('\n') else rendered

    def __call__(self):
        return self.get_content()
