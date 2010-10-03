# This file is part of Static Sauce <http://github.com/jdufresne/staticsauce>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import uuid

def slug_from_filename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def get_element_text(document, name):
    nodes = document.getElementsByTagName(name)
    if len(nodes) != 1:
        raise KeyError(name)
    node = nodes[0]
    return ''.join([child_node.toxml() for child_node in node.childNodes])

def rfc3339(datetime):
    return datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

def atom_uuid(url):
    return uuid.uuid5(uuid.NAMESPACE_URL, url).urn
