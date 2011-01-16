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
from staticsauce.files import StaticFile
from staticsauce.templating import render
from staticsauce.modules.gallery import models


def albums():
    return StaticFile(render('/gallery/albums.html', {
        'albums': models.albums(),
    }))


def album(slug):
    return StaticFile(render('/gallery/album.html', {
        'album': models.album(slug),
    }))


def photo(album_slug, slug):
    return StaticFile(render('/gallery/photo.html', {
        'photo': models.album(album_slug).photo(slug),
    }))


def image(album_slug, slug, thumbnail=False):
    size = \
        (settings.gallery.THUMBNAIL_WIDTH, settings.gallery.THUMBNAIL_HEIGHT) \
            if thumbnail \
            else (settings.gallery.IMAGE_WIDTH, settings.gallery.IMAGE_HEIGHT)

    image = _preprocess_image(
        _image_filename(album_slug, slug),
        size,
        settings.gallery.QUALITY,
        thumbnail and settings.gallery.CROP_THUMBNAIL
    )

    stringio = StringIO.StringIO()
    image.save(stringio, 'JPEG', quality=settings.gallery.QUALITY)
    contents = stringio.getvalue()
    stringio.close()

    return StaticFile(contents)


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
