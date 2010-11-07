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


import errno
import logging
import shutil
from staticsauce.conf import settings
from staticsauce.utils import import_path


def preprocess():
    try:
        shutil.rmtree(settings.BUILD_DIR)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
    shutil.copytree(settings.PUBLIC_DIR, settings.BUILD_DIR)

    for module in settings.MODULES:
        logging.info("preprocess %(module)s", {
            'module': module,
        })
        module = import_path(module, 'events', always_fail=False)
        if module:
            module.preprocess()
