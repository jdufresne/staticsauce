from staticsauce import config

class Route:
    def __init__(self, filename, controller, action, permutations):
        self.filename = filename
        self.controller = controller
        self.action = action
        self.permutations = permutations


class RouteMapper:
    def __init__(self):
        self._routes = {}

    def add(self, name, filename, controller, action, permutations=None):
        if name in self._routes:
            raise KeyError(name)
        self._routes[name] = Route(filename, controller, action, permutations)

    def extend(self, prefix, mapper):
        for name, route in mapper.routes():
            filename = prefix + route.filename
            self.add(name, filename, route.controller, route.action,
                     route.permutations)

    def routes(self):
        return self._routes.iteritems()

    def __iter__(self):
        return self._routes.itervalues()

    def __getitem__(self, name):
        return self._routes[name]


_mapper = None
def init():
    global _mapper

    module_name = config.get('project', 'routes')
    module = __import__(module_name)
    components = module_name.split('.')
    for component in components[1:]:
        module = getattr(module, component)
    _mapper = module.mapper()

def mapper():
    return _mapper

def url(name, **kwargs):
    return (config.get('site', 'site_root') +
            _mapper[name].filename.format(**kwargs))
