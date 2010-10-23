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
import ConfigParser

_config = None
_defaults = {}

def init(filename):
    global _config
    global _defaults

    _defaults['project_dir'] = os.path.abspath(os.path.dirname(filename))
    _config = ConfigParser.SafeConfigParser(_defaults)
    _config.read(filename)


def get(section, key, default=None):
    def get_default():
        if default is None:
            raise
        return default

    try:
        value = _config.get(section, key)
    except ConfigParser.NoSectionError:
        value = get_default()
    except ConfigParser.NoOptionError:
        value = get_default()
    return value


def modules():
    modules = []

    try:
        items = _config.items('modules')
    except ConfigParser.NoSectionError:
        pass
    else:
        for name, path in items:
            if name not in _defaults:
                if not path:
                    path = '.'.join(['staticsauce', 'modules', name])
                modules.append((name, path))

    return modules
