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
from staticsauce.utils import import_path


try:
    import settings
except ImportError:
    traceback = sys.exc_info()[2]
    if traceback.tb_next:
        raise
    settings = None


if settings is not None:
    for module in settings.MODULES:
        module_parts = module.rsplit('.', 1)
        module_name = module_parts[-1]
        if not hasattr(settings, module_name):
            module = import_path(module, 'settings', always_fail=False)
            if module:
                setattr(settings, module_name, module)
