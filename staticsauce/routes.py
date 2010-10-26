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
from staticsauce import config
from staticsauce import utils


class Route(object):
    def __init__(self, filename, controller, action, permutations, **kwargs):
        self.filename = filename
        self.controller = controller
        self.action = action
        self.permutations = permutations
        self.kwargs = kwargs


class RouteMapper(object):
    def __init__(self):
        self._routes = {}

    def add(self, name, filename, controller, action,
            permutations=None, **kwargs):
        if name in self._routes:
            raise KeyError(name)
        self._routes[name] = Route(
            filename,
            controller,
            action,
            permutations,
            **kwargs
        )

    def extend(self, prefix, mapper):
        for name, route in mapper.routes():
            filename = prefix + route.filename
            self.add(
                name,
                filename,
                route.controller,
                route.action,
                route.permutations,
                **route.kwargs
            )

    def routes(self):
        return self._routes.iteritems()

    def __iter__(self):
        return self._routes.itervalues()

    def url(self, name, **kwargs):
        site_root = config.get('site', 'site_root')
        return site_root + self._routes[name].filename.format(**kwargs)


def init():
    module = utils.import_path(config.get('project', 'routes'))
    mapper = module.mapper()

    sys.modules[__name__].mapper = lambda: mapper
    sys.modules[__name__].url = mapper.url
