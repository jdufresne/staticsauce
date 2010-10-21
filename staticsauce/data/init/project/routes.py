from staticsauce import routes

def mapper():
    mapper = routes.RouteMapper()
    mapper.add(
        'index',
        '/index.html',
        controller='simple',
        action='direct_to_template',
        permutations=[
            {'template': '/index.html'}
        ]
    )
    return mapper
