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
from staticsauce import config
from staticsauce import routes
from staticsauce import commands
from staticsauce.events import preprocess

class BuildCommand(commands.Command):
    command = 'build'

    def __call__(self, **kwargs):
        preprocess()

        print 'building'
        build_dir = config.get('project', 'build_dir')
        for route in routes.mapper():
            filename = build_dir
            for component in route.filename.split(os.sep):
                filename = os.path.join(filename, component)

            controller = self.get_controller(route.controller)
            action = getattr(controller, route.action)

            if route.permutations is not None:
                for permutation in route.permutations:
                    fmt_filename = filename.format(**permutation)

                    try:
                        os.makedirs(os.path.dirname(fmt_filename))
                    except OSError as e:
                        if e.errno != errno.EEXIST:
                            raise e

                    with open(fmt_filename, 'w') as f:
                        f.write(action(**permutation))
            else:
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise e

                with open(filename, 'w') as f:
                    f.write(action())

    def get_controller(self, controller):
        for name, path in config.modules():
            path = '.'.join([path, 'controllers', controller])
            try:
                module = __import__(path)
            except ImportError:
                pass
            else:
                components = path.split('.')
                for component in components[1:]:
                    module = getattr(module, component)

                return module.__controller__()

        raise ImportError("No module named {name}".format(name=controller))
