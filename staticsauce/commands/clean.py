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

import shutil
import errno
from staticsauce import commands
from staticsauce.conf import settings

class CleanCommand(commands.Command):
    command = 'clean'

    def __call__(self):
        print "cleaning {build_dir}".format(build_dir=settings.BUILD_DIR)

        try:
            shutil.rmtree(settings.BUILD_DIR)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise e
