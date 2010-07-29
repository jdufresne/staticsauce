import os


class Route:
    def __init__(self, url, filename, template, **kwargs):
        self.url = url
        self.filename = filename
        self.template = template
        self.kwargs = kwargs


class RouteMapper:
    def __init__(self):
        self._routes = []

    def add(self, url, filename, template, **kwargs):
        self._routes.append(Route(url, filename, template, **kwargs))

    def extend(self, prefix, mapper):
        self._routes.extend(map(lambda route: Route(prefix + route.url,
                                                    prefix + route.filename,
                                                    route.template,
                                                    **route.kwargs), mapper))

    def __iter__(self):
        return self._routes.__iter__()
