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
from staticsauce.conf import settings
from staticsauce.utils import path_append, import_path


class Route(object):
    def __init__(self, filename, controller, permutations, **kwargs):
        self.filename = filename
        self.controller = controller
        self.permutations = permutations
        self.kwargs = kwargs


class RouteMapper(object):
    def __init__(self):
        self._routes = {}

    def add(self, name, filename, controller, permutations=None, **kwargs):
        if name in self._routes:
            raise KeyError(name)
        self._routes[name] = Route(
            filename,
            controller,
            permutations,
            **kwargs
        )

    def extend(self, path, prefix=None):
        module = import_path(path)
        mapper = module.mapper()

        for name, route in mapper.routes():
            filename = route.filename
            if prefix is not None:
                filename = path_append(prefix, filename)
            self.add(
                name,
                filename,
                route.controller,
                route.permutations,
                **route.kwargs
            )

    def routes(self):
        return iter(self._routes.items())

    def __iter__(self):
        return iter(self._routes.values())

    def url(self, name, **kwargs):
        return path_append(
            settings.SITE_ROOT,
            self._routes[name].filename.format(**kwargs)
        )


if settings is not None:
    module = import_path(settings.ROUTES)
    mapper = module.mapper()
