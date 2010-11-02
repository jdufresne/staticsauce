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
from PIL import Image
from staticsauce.conf import settings
from staticsauce.modules.gallery import models


def crop_center(image, size):
    left = (image.size[0] - size[0]) / 2 if image.size[0] > size[0] else 0
    top = (image.size[1] - size[1]) / 2 if image.size[1] > size[1] else 0
    box = left, top, left + size[0], top + size[1]
    return image.crop(box)


def resize(image, size, max=True):
    if max and image.size[0] >= image.size[1] or \
            not max and image.size[1] >= image.size[0]:
        width = size[0]
        height = width * image.size[1] / image.size[0]
    else:
        height = size[1]
        width = height * image.size[0] / image.size[1]
    return image.resize((width, height), Image.ANTIALIAS)


def preprocess():
    image_size = (
        settings.gallery.IMAGE_WIDTH,
        settings.gallery.IMAGE_HEIGHT,
    )
    thumbnail_size = (
        settings.gallery.THUMBNAIL_WIDTH,
        settings.gallery.THUMBNAIL_HEIGHT,
    )

    gallery_dir = os.path.join(settings.BUILD_DIR, 'images', 'gallery')
    os.makedirs(gallery_dir)

    for album in models.albums():
        album_data_dir = os.path.join(
            settings.DATA_DIR,
            'gallery',
            'images',
            album.slug
        )
        album_dir = os.path.join(gallery_dir, album.slug)
        thumbnail_dir = os.path.join(album_dir, 'thumbnails')

        os.mkdir(album_dir)
        os.mkdir(thumbnail_dir)

        for index, filename in enumerate(sorted(os.listdir(album_data_dir))):
            print "processing %s" % filename

            image = Image.open(os.path.join(album_data_dir, filename))
            filename = '{album}{index}.jpeg'.format(
                album=album.slug,
                index=index
            )

            scaled_image = resize(image, image_size)
            scaled_image.save(
                os.path.join(album_dir, filename),
                'JPEG',
                quality=settings.gallery.QUALITY,
            )
            print "scaled %s %s -> %s" % (
                filename,
                str(image.size),
                str(scaled_image.size),
            )

            scaled_image = resize(
                image,
                thumbnail_size,
                not settings.gallery.CROP_THUMBNAIL
            )

            if settings.gallery.CROP_THUMBNAIL:
                scaled_image = crop_center(scaled_image, thumbnail_size)

            scaled_image.save(
                os.path.join(thumbnail_dir, filename),
                'JPEG',
                quality=settings.gallery.QUALITY,
            )
            print "scaled %s %s -> %s" % (
                filename,
                str(image.size),
                str(scaled_image.size),
            )
