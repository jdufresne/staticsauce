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
import sys
import ConfigParser


class StaticSauceConfig(object):
    def __init__(self, filename):
        self.defaults = {
            'project_dir': os.path.abspath(os.path.dirname(filename))
        }
        self.config = ConfigParser.SafeConfigParser(self.defaults)
        self.config.read(filename)

    def get(self, section, key, default=None):
        def get_default():
            if default is None:
                raise
            return default

        try:
            value = self.config.get(section, key)
        except ConfigParser.NoSectionError:
            value = get_default()
        except ConfigParser.NoOptionError:
            value = get_default()
        return value

    def modules(self):
        modules = []
        try:
            items = self.config.items('modules')
        except ConfigParser.NoSectionError:
            pass
        else:
            for name, path in items:
                if name not in self.defaults:
                    if not path:
                        path = '.'.join(['staticsauce', 'modules', name])
                    modules.append((name, path))
        return modules


def init(filename):
    config = StaticSauceConfig(filename)

    sys.modules[__name__].get = config.get
    sys.modules[__name__].modules = config.modules
