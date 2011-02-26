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


from staticsauce.feed import Feed
from staticsauce.modules.gallery import models
from staticsauce.conf import settings


class AlbumFeed(Feed):
    title = "{}'s photos".format(settings.AUTHOR)
    content_template = '/gallery/feeds/album/content.html'

    def entries(self):
        return models.albums()

    def entry_title(self, album):
        return album.title

    def entry_updated(self, album):
        return album.date

    def entry_content(self, album):
        return album.description
