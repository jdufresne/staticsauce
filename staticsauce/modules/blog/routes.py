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


from staticsauce.routes import RouteMapper
from staticsauce.modules.blog import models


def mapper():
    mapper = RouteMapper()
    articles = models.articles()
    mapper.add(
        'article',
        '/articles/{slug}.html',
        'staticsauce.modules.blog.controllers.article',
        permutations=[{'slug': article.slug} for article in articles]
    )
    return mapper
