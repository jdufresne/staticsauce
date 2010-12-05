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


from staticsauce.conf import settings


class StaticFile(object):
    def save(self, filename):
        raise NotImplementedError


class HTMLFile(StaticFile):
    def __init__(self, contents):
        super(HTMLFile, self).__init__()
        self.contents = contents

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.contents)


class JPEGFile(StaticFile):
    def __init__(self, image):
        super(JPEGFile, self).__init__()
        self.image = image

    def save(self, filename):
        self.image.save(filename, 'JPEG', quality=settings.gallery.QUALITY)
