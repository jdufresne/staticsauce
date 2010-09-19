from jinja2 import Environment, FileSystemLoader
from staticsauce.templating.templaterenderer import TemplateRenderer
from staticsauce import config
from staticsauce import routes


class Jinja2TemplateRenderer(TemplateRenderer):
    def __init__(self):
        loader = FileSystemLoader(config.get('project', 'template_dir'))
        self.env = Environment(loader=loader)
        self.env.globals = {
            'AUTHOR': config.get('author', 'name'),
            'AUTHOR_EMAIL': config.get('author', 'email'),
            'SITE_DOMAIN': config.get('site', 'site_domain'),
            'SITE_ROOT': config.get('site', 'site_root'),
            'url': routes.url,
        }

    def render(self, template, **kwargs):
        template = self.env.get_template(template)
        return template.render(**kwargs)
