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
import datetime
import xml.dom.minidom
from staticsauce import config
from staticsauce.helpers import get_element_text, slug_from_filename

def parse_album(filename):
    albums_dir = os.path.join(config.get('project', 'data_dir'),
                              'photo', 'albums')
    document = xml.dom.minidom.parse(os.path.join(albums_dir, filename))
    slug = slug_from_filename(filename)
    title = get_element_text(document, 'title')
    year, month, day = map(int, get_element_text(document, 'date').split('-'))
    date = datetime.date(year, month, day)
    album = Album(slug, title, date)

    cover = get_element_text(document, 'cover')

    return album, cover


def photos(album, cover_filename):
    photos = []
    cover = None
    images_dir = os.path.join(config.get('project', 'data_dir'),
                              'photo', 'images', album.slug)

    for index, filename in enumerate(sorted(os.listdir(images_dir))):
        slug = '{album}{index}'.format(album=album.slug, index=index)
        photo = Photo(slug, album)

        if cover_filename == filename:
            cover = photo

        photos.append(photo)

    return photos, cover


def albums():
    albums = []
    albums_dir = os.path.join(config.get('project', 'data_dir'),
                              'photo', 'albums')

    for filename in os.listdir(albums_dir):
        album, cover = parse_album(filename)
        album.photos, album.cover = photos(album, cover)
        albums.append(album)
    return sorted(albums, key=lambda album: album.date, reverse=True)


def album(slug):
    album, cover = parse_album('.'.join([slug, 'xml']))
    album.photos, album.cover = photos(album, cover)
    return album


class Album:
    def __init__(self, slug, title, date):
        self.slug = slug
        self.title = title
        self.date = date
        self.cover = None
        self.photos = None

    def add_photo(self, photo):
        photo.album = self
        self.photos.append(photo)

    def images(self):
        url = '{site_root}/images/photo/{slug}'
        return url.format(site_root=config.get('site', 'site_root'),
                          slug=self.slug)

    def photo(self, photo_slug):
        for photo in self.photos:
            if photo.slug == photo_slug:
                return photo
        raise KeyError

class Photo:
    def __init__(self, slug, album):
        self.slug = slug
        self.album = album

    def thumbnail(self):
        url = '{images}/thumbnails/{slug}.jpeg'
        return url.format(images=self.album.images(), slug=self.slug)

    def image(self):
        url = '{images}/{slug}.jpeg'
        return url.format(images=self.album.images(), slug=self.slug)

    def prev(self):
        index = self.album.photos.index(self)
        index = (index - 1) % len(self.album.photos)
        return self.album.photos[index]

    def next(self):
        index = self.album.photos.index(self)
        index = (index + 1) % len(self.album.photos)
        return self.album.photos[index]
