from staticsauce.routes import RouteMapper
from staticsauce.modules.photo import models


ALBUMS_URL = '/albums'
ALBUMS_FILENAME = '/albums.html'

ALBUM_URL = '/albums/{album}'
ALBUM_FILENAME = '/albums/{album}.html'

PHOTO_URL = '/albums/{album}/{photo}'
PHOTO_FILENAME = '/albums/{album}/{photo}.html'


def mapper():
    mapper = RouteMapper()

    albums = models.albums()
    mapper.add(ALBUMS_URL, ALBUMS_FILENAME,
               template='/photo/albums.html', albums=albums)
    for album in albums:
        url = ALBUM_URL.format(album=album.slug)
        filename = ALBUM_FILENAME.format(album=album.slug)
        mapper.add(url, filename,
                   template='/photo/album.html', album=album)


        for photo in album.photos:
            url = PHOTO_URL.format(album=album.slug, photo=photo.slug)
            filename = PHOTO_FILENAME.format(album=album.slug,
                                             photo=photo.slug)
            mapper.add(url, filename,
                       template='/photo/photo.html', photo=photo)
    return mapper
