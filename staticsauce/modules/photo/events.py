import os
import shutil
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
    os.mkdir(photo_dir)
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
