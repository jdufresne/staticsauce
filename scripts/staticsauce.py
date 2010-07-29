import errno
import sys
import shutil

from staticsauce import config
from staticsauce import templating
from staticsauce.commands.build import build


def preprocess():
    try:
        shutil.rmtree(config.get('project', 'build_dir'))
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
    shutil.copytree(config.get('project', 'public_dir'),
                    config.get('project', 'build_dir'))

    for name, path in config.modules():
        module = __import__(path)
        names = path.split('.')
        for name in names[1:]:
            module = getattr(module, name)

        try:
            module_preprocess = module.events.preprocess
        except AttributeError:
            pass
        else:
            print "preprocess", module.__name__
            module_preprocess()

def main():
    config_filename = sys.argv[1]
    config.init(config_filename)
    templating.init()

    preprocess()
    build()

if __name__ == '__main__':
    main()
