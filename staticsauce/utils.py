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


def import_path(*args, **kwargs):
    path = '.'.join(args)
    try:
        module = __import__(path, None, None, None, 0)
    except ImportError as e:
        try:
            always_fail = kwargs['always_fail']
        except KeyError:
            always_fail = True
        try:
            type, value, tb = sys.exc_info()
            if tb.tb_next or always_fail:
                raise e
        finally:
            del tb
        module = None
    else:
        components = path.split('.')
        for component in components[1:]:
            module = getattr(module, component)
    return module


def path_append(root, path):
    if root:
        components = [root]
        components.extend(path.split(os.sep))
        path = os.path.join(*components)
    return path
