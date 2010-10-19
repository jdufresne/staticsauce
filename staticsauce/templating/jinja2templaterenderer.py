# This file is part of Static Sauce <http://github.com/jdufresne/staticsauce>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from jinja2 import Environment, FileSystemLoader
from staticsauce.templating.templaterenderer import TemplateRenderer
from staticsauce.templating import filters
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

        # make registration a decorator
        self.env.filters['paragraphs'] = filters.paragraphs


    def render(self, template, **kwargs):
        template = self.env.get_template(template)
        return template.render(**kwargs)
