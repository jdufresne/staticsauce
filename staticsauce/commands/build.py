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
import shutil
from staticsauce import commands
from staticsauce import routes
from staticsauce.conf import settings
from staticsauce.exceptions import AlreadyUpdatedError
from staticsauce.files import StaticFile
from staticsauce.utils import import_path, path_append, file_updated


class BuildCommand(commands.Command):
    command = 'build'

    def copy_public_dir(self):
        for src_dir, dirnames, filenames in os.walk(settings.PUBLIC_DIR):
            dest_dir = path_append(
                settings.BUILD_DIR,
                src_dir[len(settings.PUBLIC_DIR):]
            )
            try:
                os.mkdir(dest_dir)
            except OSError as err:
                if err.errno != errno.EEXIST:
                    raise
            for filename in filenames:
                dest_path = os.path.join(dest_dir, filename)
                src_path = os.path.join(src_dir, filename)
                if file_updated(dest_path, src_path):
                    self.logger.info("[copy] %(src)s %(dest)s", {
                        'src': src_path,
                        'dest': dest_path,
                    })
                    shutil.copy(src_path, dest_dir)

    def __call__(self):
        self.copy_public_dir()
        for name, route in routes.mapper:
            filename = path_append(settings.BUILD_DIR, route.filename)
            module, controller = route.controller.rsplit('.', 1)
            module = import_path(module)
            controller = getattr(module, controller)

            permutations = route.permutations \
                if route.permutations is not None else [{}]

            for permutation in permutations:
                fmt_filename = filename.format(**permutation)

                try:
                    os.makedirs(os.path.dirname(fmt_filename))
                except OSError as err:
                    if err.errno != errno.EEXIST:
                        raise

                uri = 'http://{domain}{path}'.format(
                    domain=settings.SITE_DOMAIN,
                    path=route.filename
                )
                static_file = StaticFile(fmt_filename, uri)

                kwargs = {}
                if route.kwargs:
                    kwargs.update(route.kwargs)
                kwargs.update(permutation)

                try:
                    controller(static_file, **kwargs)
                except AlreadyUpdatedError:
                    pass
                else:
                    self.logger.info("[%(controller)s] %(filename)s", {
                        'controller': route.controller,
                        'filename': fmt_filename,
                    })
                    static_file.save(fmt_filename)
