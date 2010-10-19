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

from staticsauce import config
from staticsauce.modules.photo import models

IMAGE_SIZE = (720, 720)
THUMBNAIL_SIZE = (128, 128)
QUALITY = 95

def resize(image, size):
    if image.size[0] >= image.size[1]:
        width = size[0]
        height = width * image.size[1] / image.size[0]
    else:
        height = size[1]
        width = height * image.size[0] / image.size[1]
    return image.resize((width, height), Image.ANTIALIAS)

def preprocess():
    photo_dir = os.path.join(config.get('project', 'build_dir'),
                             'images', 'photo')
    os.makedirs(photo_dir)
    for album in models.albums():
        album_data_dir = os.path.join(
            config.get('project', 'data_dir'),
            'photo',
            'images',
            album.slug
        )
        album_dir = os.path.join(photo_dir, album.slug)
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

            scaled_image = resize(image, IMAGE_SIZE)
            scaled_image.save(
                os.path.join(album_dir, filename),
                'JPEG',
                quality=QUALITY,
            )
            print "scaled %s %s -> %s" % (
                filename,
                str(image.size),
                str(scaled_image.size),
            )

            scaled_image = resize(image, THUMBNAIL_SIZE)
            scaled_image.save(
                os.path.join(thumbnail_dir, filename),
                'JPEG',
                quality=QUALITY,
            )
            print "scaled %s %s -> %s" % (
                filename,
                str(image.size),
                str(scaled_image.size),
            )
