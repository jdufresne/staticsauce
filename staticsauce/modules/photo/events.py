import os
import shutil
from PIL import Image

from staticsauce import config
from staticsauce.modules.photo import models


IMAGE_SIZE = (720, 720)
THUMBNAIL_SIZE = (128, 128)


def preprocess():
    photo_dir = os.path.join(config.get('project', 'build_dir'),
                             'images', 'photo')
    os.mkdir(photo_dir)
    for album in models.albums():
        album_data_dir = os.path.join(config.get('project', 'data_dir'),
                                      'photo', 'images', album.slug)
        album_dir = os.path.join(photo_dir, album.slug)
        thumbnail_dir = os.path.join(album_dir, 'thumbnails')

        os.mkdir(album_dir)
        os.mkdir(thumbnail_dir)

        for index, filename in enumerate(sorted(os.listdir(album_data_dir))):
            print "processing", filename

            image = Image.open(os.path.join(album_data_dir, filename))
            filename = '{album}{index}.jpeg'.format(album=album.slug,
                                                    index=index)
            image.thumbnail(IMAGE_SIZE)
            image.save(os.path.join(album_dir, filename))
            image.thumbnail(THUMBNAIL_SIZE)
            image.save(os.path.join(thumbnail_dir, filename))
