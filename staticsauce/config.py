import os
import ConfigParser


_config = None
_defaults = {}

def init(filename):
    global _config
    global _defaults

    _defaults['project_dir'] = os.path.abspath(os.path.dirname(filename))
    _config = ConfigParser.SafeConfigParser(_defaults)
    _config.read(filename)

def get(section, key):
    return _config.get(section, key)

def modules():
    modules = []
    for name, path in _config.items('modules'):
        if name not in _defaults:
            if not path:
                path = '.'.join(['staticsauce', 'modules', name])
            modules.append((name, path))
    return modules
