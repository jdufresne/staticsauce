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


import os
import functools
import re
import jinja2
from staticsauce import routes
from staticsauce.conf import settings
from staticsauce.utils import import_path


class TemplateRenderer(object):
    def __init__(self):
        search_path = [settings.TEMPLATE_DIR]
        for module in settings.MODULES:
            path = os.path.join(
                os.path.abspath(os.path.dirname(import_path(module).__file__)),
                'templates'
            )
            if os.path.isdir(path):
                search_path.append(path)
        loader = jinja2.FileSystemLoader(search_path)

        self.env = jinja2.Environment(
            trim_blocks=True,
            undefined=jinja2.StrictUndefined,
            autoescape=True,
            loader=loader
        )

        self.env.globals.update({
            'AUTHOR': settings.AUTHOR,
            'AUTHOR_EMAIL': settings.AUTHOR_EMAIL,
            'SITE_ROOT': settings.SITE_ROOT,
            'url': routes.mapper.url,
        })

        self.env.filters.update({
            'paragraphs': paragraphs,
        })

        for module in settings.MODULES:
            module = import_path(module, 'templating', always_fail=False)
            if module:
                self.env.globals.update(module.context_processor())

    def render(self, template, context=None):
        if context is None:
            context = {}
        template = self.env.get_template(template)
        return template.render(context)


def autoescapefilter(func):
    @jinja2.evalcontextfilter
    @functools.wraps(func)
    def new_func(eval_ctx, *args, **kwargs):
        result = func(*args, **kwargs)
        if eval_ctx.autoescape:
            result = jinja2.Markup(result)
        return result
    return new_func


def autoescapefunction(func):
    @jinja2.evalcontextfunction
    @functools.wraps(func)
    def new_func(eval_ctx, *args, **kwargs):
        result = func(*args, **kwargs)
        if eval_ctx.autoescape:
            result = jinja2.Markup(result)
        return result
    return new_func


@autoescapefilter
def paragraphs(value, _re=re.compile(r'(?:\r\n|\r|\n){2,}')):
    if value:
        value = value.strip()

    if not value:
        return ''

    return ''.join(
        '<p>{p}</p>'.format(p=paragraph.strip())
        for paragraph in _re.split(jinja2.escape(value))
    )


def inclusiontag(template):
    def decorator(func):
        @autoescapefunction
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            context = func(*args, **kwargs)
            return render(template, context)
        return new_func
    return decorator


render = TemplateRenderer().render
