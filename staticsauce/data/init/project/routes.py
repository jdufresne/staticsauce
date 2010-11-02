from staticsauce.routes import RouteMapper


def mapper():
    mapper = RouteMapper()
    mapper.add(
        'index',
        '/index.html',
        'staticsauce.controllers.simple.direct_to_file',
        template='/index.html'
    )
    return mapper
