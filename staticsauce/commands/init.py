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
import staticsauce
from staticsauce import commands

class InitCommand(commands.Command):
    command = 'init'
    config = False

    def init_parser(self, parser):
        super(InitCommand, self).init_parser(parser)
        parser.add_argument('name')

    def __call__(self, name):
        print "initializing project {name}".format(name=name)

        shutil.copytree(
            os.path.join(
                os.path.dirname(staticsauce.__file__),
                'data',
                'init'
            ),
            name
        )