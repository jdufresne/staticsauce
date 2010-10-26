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
VERSION = '0.2.1'
URL = 'http://pypi.python.org/pypi/{name}'
DOWNLOAD_URL = 'http://pypi.python.org/packages/source/s/{name}/{name}-{version}.tar.gz'


if __name__ == '__main__':
    setup(
        name=NAME,
        version=VERSION,
        description='Static Sauce Website Generator',
        long_description=open('README').read(),
        author='Jon Dufresne',
        author_email='jon.dufresne@gmail.com',
        url=URL.format(name=NAME),
        download_url=DOWNLOAD_URL.format(name=NAME, version=VERSION),
        packages=[
            'staticsauce',
            'staticsauce.commands',
            'staticsauce.controllers',
            'staticsauce.modules',
            'staticsauce.modules.photo',
            'staticsauce.modules.photo.controllers',
            'staticsauce.templating',
        ],
        package_dir={'staticsauce': 'staticsauce'},
        package_data={
            'staticsauce': [
                'data/init/development.conf',
                'data/init/project/__init__.py',
                'data/init/project/controller.py',
                'data/init/project/routes.py',
                'data/init/public/styles/project.css',
                'data/init/templates/base.html',
                'data/init/templates/index.html',
            ]
        },
        scripts=['scripts/staticsauce'],
    )
