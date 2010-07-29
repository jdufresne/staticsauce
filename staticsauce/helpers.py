import os

def slug_from_filename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def get_element_text(document, name):
    nodes = document.getElementsByTagName(name)
    if len(nodes) != 1:
        raise KeyError(name)
    node = nodes[0]
    return ''.join([child_node.toxml() for child_node in node.childNodes])
