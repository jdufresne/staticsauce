from staticsauce.controller import Controller
from staticsauce import templating
from staticsauce.modules.photo import models
from staticsauce.helpers import *


class PhotoController(Controller):
    def albums(self):
        render = templating.render_jinja2
        return render('/photo/albums.html', albums=models.albums())

    def album(self, slug):
        render = templating.render_jinja2
        album = models.album(slug)
        return render('/photo/album.html', album=album)

    def photo(self, album_slug, slug):
        render = templating.render_jinja2
        album = models.album(album_slug)
        photo = album.photo(slug)
        return render('/photo/photo.html', photo=photo)

    def feed(self):
        render = templating.render_jinja2
        albums = albums=models.albums()
        most_recent = min(albums, key=lambda x: x.date)
        updated = most_recent.date
        return render(
            '/photo/feed.xml',
            atom_uuid=atom_uuid,
            rfc3339=rfc3339,
            updated=updated,
            albums=albums
        )


__controller__ = PhotoController
