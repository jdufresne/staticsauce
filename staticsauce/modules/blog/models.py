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
import docutils.core
from staticsauce.conf import settings
from staticsauce.utils import import_path


def articles():
    module = import_path('data.blog')
    return sorted(
        module.articles,
        key=lambda article: article.date, reverse=True
    )


def article(slug):
    for article in articles():
        if article.slug == slug:
            return article
    raise KeyError(slug)


class Article(object):
    def __init__(self, slug, title, date):
        self.slug = slug
        self.title = title
        self.date = date

    def html(self):
        path = os.path.join(
            settings.DATA_DIR,
            'blog',
            'articles',
            '.'.join([self.slug, 'rst'])
        )

        parts = docutils.core.publish_parts(
            source=open(path).read(),
            source_path=path,
            writer_name='html',
        )

        return parts['body']
