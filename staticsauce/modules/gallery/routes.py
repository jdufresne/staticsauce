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


from staticsauce.routes import RouteMapper
from staticsauce.modules.gallery import models


def mapper():
    mapper = RouteMapper()
    albums = models.albums()
    photo_permutations = [
        {'album_slug': album.slug, 'slug': photo.slug}
        for album in albums for photo in album.photos
    ]

    mapper.add(
        'albums',
        '/albums.html',
        controller='staticsauce.modules.gallery.controllers.albums'
    )
    mapper.add(
        'album',
        '/albums/{slug}.html',
        controller='staticsauce.modules.gallery.controllers.album',
        permutations=[{'slug': album.slug} for album in albums]
    )
    mapper.add(
        'photo',
        '/albums/{album_slug}/{slug}.html',
        controller='staticsauce.modules.gallery.controllers.photo',
        permutations=photo_permutations
    )
    mapper.add(
        'image',
        '/images/gallery/{album_slug}/{slug}.jpeg',
        controller='staticsauce.modules.gallery.controllers.image',
        permutations=photo_permutations
    )
    mapper.add(
        'thumbnail',
        '/images/gallery/{album_slug}/thumbnails/{slug}.jpeg',
        controller='staticsauce.modules.gallery.controllers.image',
        permutations=photo_permutations,
        kwargs={'thumbnail': True}
    )
    return mapper
