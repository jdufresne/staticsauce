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
import uuid
import cssutils
from staticsauce.conf import settings


cssutils.ser.prefs.useMinified()


def stylesheet(static_file):
    stylesheets_dir = os.path.join(
        settings.DATA_DIR,
        'cssminify',
        'stylesheets'
    )
    imports = [
        '@import "{stylesheet}";'.format(stylesheet=stylesheet)
        for stylesheet in os.listdir(stylesheets_dir)
    ]
    proxy_stylesheet = cssutils.parseString(
        '\n'.join(imports),
        href='file://{path}'.format(
            path=os.path.join(
                stylesheets_dir,
                '{uuid}.css'.format(uuid=uuid.uuid4())
            )
        )
    )
    stylesheet = cssutils.resolveImports(proxy_stylesheet)
    static_file.content = stylesheet.cssText
