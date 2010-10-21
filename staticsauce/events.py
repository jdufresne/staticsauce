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
import shutil
from staticsauce import config

def preprocess():
    try:
        shutil.rmtree(config.get('project', 'build_dir'))
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
    shutil.copytree(
        config.get('project', 'public_dir'),
        config.get('project', 'build_dir')
    )

    for name, path in config.modules():
        module = __import__(path)
        names = path.split('.')
        for name in names[1:]:
            module = getattr(module, name)

        try:
            module_preprocess = module.events.preprocess
        except AttributeError:
            pass
        else:
            print "preprocess", module.__name__
            module_preprocess()