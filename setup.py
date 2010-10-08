#!/usr/bin/env python

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


from distutils.core import setup

NAME = 'staticsauce'
VERSION = '0.1'
URL = 'http://jondufresne.org/staticsauce.html'
DOWNLOAD_URL = 'http://jondufresne.org/staticsauce/{name}-{version}.tar.gz'

if __name__ == '__main__':
    setup(
        name=NAME,
        version=VERSION,
        description='Static Sauce Website Generator',
        author='Jon Dufresne',
        author_email='jon.dufresne@gmail.com',
        url=URL,
        download_url=DOWNLOAD_URL.format(name=NAME, version=VERSION),
        packages=[
            'staticsauce',
            'staticsauce.commands',
            'staticsauce.modules',
            'staticsauce.modules.photo',
            'staticsauce.modules.photo.controllers',
            'staticsauce.templating',
        ],
        scripts=['scripts/staticsauce'],
    )
