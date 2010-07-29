import os
import errno
import routes

from staticsauce import config
from staticsauce import templating


def build():
    render = templating.render_jinja2
    for route in routes.mapper():
        print "creating", route.filename
        filename = os.path.join(config.get('project', 'build_dir'),
                                *route.filename.split(os.sep))

        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open(filename, 'w') as f:
            f.write(render(route.template, **route.kwargs))
