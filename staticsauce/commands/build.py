import os
import errno

from staticsauce import config
from staticsauce import routes


def build():
    print 'building'
    build_dir = config.get('project', 'build_dir')
    for route in routes.mapper():
        filename = build_dir
        for component in route.filename.split(os.sep):
            filename = os.path.join(filename, component)



        controller = get_controller(route.controller)
        action = getattr(controller, route.action)

        if route.permutations is not None:
            for permutation in route.permutations:
                fmt_filename = filename.format(**permutation)

                try:
                    os.makedirs(os.path.dirname(fmt_filename))
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise e

                with open(fmt_filename, 'w') as f:
                    f.write(action(**permutation))
        else:
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise e

            with open(filename, 'w') as f:
                f.write(action())

def get_controller(controller):
    for name, path in config.modules():
        path = '.'.join([path, 'controllers', controller])
        try:
            module = __import__(path)
        except ImportError:
            pass
        else:
            components = path.split('.')
            for component in components[1:]:
                module = getattr(module, component)
            return module.__controller__()
    raise ImportError("No module named {name}".format(name=controller))
