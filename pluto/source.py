
__all__ = ["Source", "Template"]

from pluto.environment import env

class Source(object):
    def get_content(self):
        raise NotImplementedError()

    def get_checksum(self):
        return None

class Template(Source):
    def __init__(self, name, variables=None):
        self.name = name
        self.variables = variables or {}

    def get_content(self):
        from jinja2 import Environment, FileSystemLoader
        template_env = Environment(loader=FileSystemLoader(env.path), autoescape=False)
        template = template_env.get_template(self.name)
        context = self.variables.copy()
        context['env'] = env
        rendered = template.render(context)
        return rendered + "\n" if not rendered.endswith('\n') else rendered

    def __call__(self):
        return self.get_content()
