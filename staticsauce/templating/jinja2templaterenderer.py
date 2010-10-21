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


import re
import jinja2
from staticsauce import config
from staticsauce import routes
from staticsauce.templating.templaterenderer import TemplateRenderer
from staticsauce.templating import filters


class Jinja2TemplateRenderer(TemplateRenderer):
    def __init__(self):
        loader = jinja2.FileSystemLoader(config.get('project', 'template_dir'))
        self.env = jinja2.Environment(loader=loader)
        self.env.globals = {
            'AUTHOR': config.get('author', 'name'),
            'AUTHOR_EMAIL': config.get('author', 'email'),
            'SITE_DOMAIN': config.get('site', 'site_domain'),
            'SITE_ROOT': config.get('site', 'site_root'),
            'url': routes.url,
        }

        self.env.filters['paragraphs'] = filters.paragraphs


    def render(self, template, context=None):
        if context is None:
            context = {}
        template = self.env.get_template(template)
        return template.render(context)


@jinja2.evalcontextfilter
def paragraphs(eval_ctx, value):
    paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
    result = ''.join('<p>{p}</p>'.format(p=paragraph.strip())
                     for paragraph in paragraph_re.split(jinja2.escape(value)))
    if eval_ctx.autoescape:
        result = jinja2.Markup(result)
    return result
