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


from staticsauce.conf import settings
from staticsauce.utils import import_path


def albums():
    module = import_path('data.gallery')
    return sorted(module.albums, key=lambda album: album.date, reverse=True)


def album(slug):
    for album in albums():
        if album.slug == slug:
          return album
    raise KeyError(slug)


class Album(object):
    def __init__(self, slug, title, date, description, photos):
        self.slug = slug
        self.title = title
        self.date = date
        self.description = description
        self.photos = photos
        self.cover = None

        for photo in photos:
            photo.album = self
            if photo.cover:
                self.cover = photo

    def photo(self, photo_slug):
        for photo in self.photos:
            if photo.slug == photo_slug:
                return photo
        raise KeyError(photo_slug)


class Photo(object):
    def __init__(self, slug, filename, description=None, cover=False):
        self.slug = slug
        self.filename = filename
        self.description = description
        self.cover = cover
        self.album = None

    def prev(self):
        index = self.album.photos.index(self)
        index = (index - 1) % len(self.album.photos)
        return self.album.photos[index]

    def next(self):
        index = self.album.photos.index(self)
        index = (index + 1) % len(self.album.photos)
        return self.album.photos[index]
