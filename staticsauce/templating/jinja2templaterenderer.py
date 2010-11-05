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


import sys
import re
import jinja2
from staticsauce import routes
from staticsauce.conf import settings
from staticsauce.templating.templaterenderer import TemplateRenderer


class Jinja2TemplateRenderer(TemplateRenderer):
    def __init__(self):
        loader = jinja2.FileSystemLoader(settings.TEMPLATE_DIR)
        self.env = jinja2.Environment(loader=loader)
        self.env.globals = {
            'AUTHOR': settings.AUTHOR,
            'AUTHOR_EMAIL': settings.AUTHOR_EMAIL,
            'SITE_ROOT': settings.SITE_ROOT,
            'url': routes.mapper.url,
        }

        self.env.filters['paragraphs'] = paragraphs
        self.env.filters['strftime'] = strftime

    def render(self, template, context=None):
        if context is None:
            context = {}
        template = self.env.get_template(template)
        return template.render(context)


@jinja2.evalcontextfilter
def paragraphs(eval_ctx, value):
    if value:
        value = value.strip()

    if not value:
        return ''

    paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
    result = ''.join(
        '<p>{p}</p>'.format(p=paragraph.strip())
        for paragraph in paragraph_re.split(jinja2.escape(value))
    )
    if eval_ctx.autoescape:
        result = jinja2.Markup(result)
    return result


def strftime(value):
    return datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
