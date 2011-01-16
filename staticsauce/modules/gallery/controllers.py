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
from PIL import Image
from staticsauce.conf import settings
from staticsauce.files import TemplateFile, JPEGFile
from staticsauce.templating import render
from staticsauce.modules.gallery import models


def albums():
    return TemplateFile('/gallery/albums.html', {
        'albums': models.albums(),
    })


def album(slug):
    return TemplateFile('/gallery/album.html', {
        'album': models.album(slug),
    })


def photo(album_slug, slug):
    return TemplateFile('/gallery/photo.html', {
        'photo': models.album(album_slug).photo(slug),
    })


def image(album_slug, slug):
    return JPEGFile(
        os.path.join(
            settings.DATA_DIR,
            'gallery',
            'images',
            album_slug,
            models.album(album_slug).photo(slug).filename
        ),
        (settings.gallery.IMAGE_WIDTH, settings.gallery.IMAGE_HEIGHT),
        settings.gallery.QUALITY
    )


def thumbnail(album_slug, slug):
    return JPEGFile(
        os.path.join(
            settings.DATA_DIR,
            'gallery',
            'images',
            album_slug,
            models.album(album_slug).photo(slug).filename
        ),
        (settings.gallery.THUMBNAIL_WIDTH, settings.gallery.THUMBNAIL_HEIGHT),
        settings.gallery.QUALITY,
        settings.gallery.CROP_THUMBNAIL
    )
