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
import StringIO
from PIL import Image
from staticsauce.conf import settings
from staticsauce.exceptions import AlreadyUpdatedError
from staticsauce.modules.gallery import models
from staticsauce.modules.gallery.feeds import AlbumFeed
from staticsauce.templating import render
from staticsauce.utils import file_updated


def albums(static_file):
    static_file.content = render('/gallery/albums.html', {
        'albums': models.albums(),
    })


def album(static_file, slug):
    static_file.content = render('/gallery/album.html', {
        'album': models.album(slug),
    })


def photo(static_file, album_slug, slug):
    static_file.content = render('/gallery/photo.html', {
        'photo': models.album(album_slug).photo(slug),
    })


def image(static_file, album_slug, slug, thumbnail=False):
    filename = _image_filename(album_slug, slug)
    if not file_updated(static_file.filename, filename):
        raise AlreadyUpdatedError

    if thumbnail:
        size = (
            settings.gallery.THUMBNAIL_WIDTH,
            settings.gallery.THUMBNAIL_HEIGHT
        )
    else:
        size = (
            settings.gallery.IMAGE_WIDTH,
            settings.gallery.IMAGE_HEIGHT
        )

    image = _preprocess_image(
        filename,
        size,
        settings.gallery.QUALITY,
        thumbnail and settings.gallery.CROP_THUMBNAIL
    )

    io = StringIO.StringIO()
    image.save(io, 'JPEG', quality=settings.gallery.QUALITY)
    static_file.content = io.getvalue()
    io.close()


def feed(static_file):
    feed = AlbumFeed(static_file.uri)
    static_file.content = feed.xml()


def _image_filename(album_slug, slug):
    return os.path.join(
        settings.DATA_DIR,
        'gallery',
        'images',
        album_slug,
        models.album(album_slug).photo(slug).filename
    )


def _preprocess_image(filename, size, quality, crop):
    image = Image.open(filename)
    scaled_image = _resize(image, size, crop)
    if crop:
        scaled_image = _crop_center(scaled_image, size)
    return scaled_image


def _resize(image, size, crop):
    if not crop and image.size[0] >= image.size[1] or \
            crop and image.size[1] >= image.size[0]:
        width = size[0]
        height = width * image.size[1] / image.size[0]
    else:
        height = size[1]
        width = height * image.size[0] / image.size[1]
    return image.resize((width, height), Image.ANTIALIAS)


def _crop_center(image, size):
    left = (image.size[0] - size[0]) / 2 \
        if image.size[0] > size[0] else 0
    top = (image.size[1] - size[1]) / 2 \
        if image.size[1] > size[1] else 0
    box = left, top, left + size[0], top + size[1]
    return image.crop(box)
