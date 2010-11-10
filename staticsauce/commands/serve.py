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
import mimetypes
import BaseHTTPServer
from staticsauce import commands
from staticsauce.conf import settings


class StaticSauceRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith(settings.SITE_ROOT):
            path = self.path[len(settings.SITE_ROOT):]
            try:
                path = os.path.join(settings.BUILD_DIR, path[1:])
                with open(path) as f:
                    content = f.read()
            except IOError:
                self.send_error(404, 'Not Found')
            else:
                self.send_response(200, 'OK')
                self.send_header('Content-type', mimetypes.guess_type(path))
                self.end_headers()
                self.wfile.write(content)
        else:
            self.send_error(404, 'Not Found')


class ServeCommand(commands.Command):
    command = 'serve'

    def __call__(self):
        httpd = BaseHTTPServer.HTTPServer(
            ('', 8000),
            StaticSauceRequestHandler
        )
        httpd.serve_forever()
