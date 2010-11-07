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


import os
import errno
import logging
import shutil
from staticsauce import commands
from staticsauce import routes
from staticsauce.conf import settings
from staticsauce.utils import import_path, path_append


class BuildCommand(commands.Command):
    command = 'build'

    def __call__(self):
        logging.info("building")

        try:
            shutil.rmtree(settings.BUILD_DIR)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
        shutil.copytree(settings.PUBLIC_DIR, settings.BUILD_DIR)

        for name, route in routes.mapper:
            logging.info('building route %(route)s', {
                'route': name,
            })
            logging.info('using controller %(controller)s', {
                'controller': route.controller,
            })

            filename = path_append(settings.BUILD_DIR, route.filename)
            module, controller = route.controller.rsplit('.', 1)
            module = import_path(module)
            controller = getattr(module, controller)

            permutations = route.permutations \
                if route.permutations is not None else [{}]

            for permutation in permutations:
                fmt_filename = filename.format(**permutation)
                logging.info("building %(filename)s", {
                    'filename': fmt_filename,
                })

                try:
                    os.makedirs(os.path.dirname(fmt_filename))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise

                kwargs = {}
                kwargs.update(route.kwargs)
                kwargs.update(permutation)
                controller(**kwargs).save(fmt_filename)
