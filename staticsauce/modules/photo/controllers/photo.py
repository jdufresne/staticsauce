from staticsauce.controller import Controller
from staticsauce import templating
from staticsauce.modules.photo import models


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

__controller__ = PhotoController
