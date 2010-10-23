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


import datetime
from staticsauce.controller import Controller
from staticsauce.templating import render
from staticsauce.modules.photo import models
from staticsauce.helpers import *


class PhotoController(Controller):
    def albums(self):
        return render('/photo/albums.html', {'albums': models.albums()})

    def album(self, slug):
        album = models.album(slug)
        return render('/photo/album.html', {'album': album})

    def photo(self, album_slug, slug):
        album = models.album(album_slug)
        photo = album.photo(slug)
        return render('/photo/photo.html', {'photo': photo})

    def feed(self):
        albums = albums=models.albums()
        most_recent = min(albums, key=lambda x: x.date) \
            if albums else datetime.datetime.now()
        updated = most_recent.date
        return render('/photo/feed.xml', {
            'atom_uuid': atom_uuid,
            'rfc3339': rfc3339,
            'updated': updated,
            'albums': albums,
        })


__controller__ = PhotoController
