from staticsauce.routes import RouteMapper
from staticsauce.modules.photo import models


def mapper():
    mapper = RouteMapper()

    albums = models.albums()

    mapper.add('albums', '/albums.html',
               controller='photo', action='albums')

    mapper.add('album', '/albums/{slug}.html',
               controller='photo', action='album',
               permutations=[{'slug': album.slug} for album in albums])

    mapper.add('photo', '/albums/{album_slug}/{slug}.html',
               controller='photo', action='photo',
               permutations=[{'album_slug': album.slug, 'slug': photo.slug}
                             for album in albums for photo in album.photos])

    return mapper
