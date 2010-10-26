def import_path(path):
    module = __import__(path)
    components = path.split('.')
    for component in components[1:]:
        module = getattr(module, component)
    return module
