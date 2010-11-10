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
import shutil
import tempfile
import staticsauce
from staticsauce import commands


class InitCommand(commands.Command):
    command = 'init'

    def init_parser(self, parser):
        parser.add_argument('name')

    def __call__(self, name):
        self.logger.info("initializing project %(name)s", {
            'name': name
        })

        # cp -r staticsauce/data/init name
        shutil.copytree(
            os.path.join(
                os.path.dirname(staticsauce.__file__),
                'data',
                'init'
            ),
            name
        )

        # mv name/project name/name
        os.rename(os.path.join(name, 'project'), os.path.join(name, name))

        # sed -e s/{project}/name/
        replace_in_file(
            os.path.join(name, 'settings.py'),
            '{project}',
            name
        )
        replace_in_file(
            os.path.join(name, 'templates', 'index.html'),
            '{project}',
            name
        )


def replace_in_file(filename, old, new):
    with tempfile.NamedTemporaryFile(delete=False) as fout:
        with open(filename) as fin:
            for line in fin:
                fout.write(line.replace(old, new))
    shutil.copyfile(fout.name, filename)
    os.remove(fout.name)
