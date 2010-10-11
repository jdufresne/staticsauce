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


import sys
import os
from staticsauce import config
from staticsauce import routes
from staticsauce import templating

class Command(object):
    config = True

    def init_parser(self, parser):
        if self.config:
            parser.add_argument('-c', '--config', default='development.conf')

    def precommand(self, **kwargs):
        if self.config:
            filename = kwargs['config']
            sys.path.insert(0, os.path.dirname(filename))
            config.init(filename)
            routes.init()
            templating.init()
