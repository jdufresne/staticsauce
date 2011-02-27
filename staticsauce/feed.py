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


import time
from xml.etree import ElementTree
from staticsauce.conf import settings
from staticsauce.templating import render


class Feed(object):
    authors = (
        (settings.AUTHOR, settings.AUTHOR_EMAIL),
    )

    _RFC3339 = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, uri):
        self.title = self.title
        self.authors = self.authors
        self.uri = uri

    def xml(self):
        root = ElementTree.Element('feed', {
            'xmlns': 'http://www.w3.org/2005/Atom',
        })

        el = ElementTree.SubElement(root, 'title')
        el.text = self.title

        el = ElementTree.SubElement(root, 'author')
        for name, email in self.authors:
            child_el = ElementTree.SubElement(el, 'name')
            child_el.text = name
            child_el = ElementTree.SubElement(el, 'email')
            child_el.text = email

        updated = max(self.entry_updated(entry) for entry in self.entries())
        el = ElementTree.SubElement(root, 'updated')
        el.text = updated.strftime(self._RFC3339)

        el = ElementTree.SubElement(root, 'id')
        el.text = self.uri

        el = ElementTree.SubElement(root, 'link', {
            'rel': 'self',
            'type': 'application/atom+xml',
            'href': self.uri,
        })

        for entry in self.entries():
            el = ElementTree.SubElement(root, 'entry')
            self.make_entry(el, entry)

        return ElementTree.tostring(root, 'UTF-8')

    def make_entry(self, el, entry):
        child_el = ElementTree.SubElement(el, 'title')
        child_el.text = self.entry_title(entry)

        child_el = ElementTree.SubElement(el, 'updated')
        child_el.text = self.entry_updated(entry).strftime(self._RFC3339)

        uri = self.entry_uri(entry)

        child_el = ElementTree.SubElement(el, 'id')
        child_el.text = uri

        child_el = ElementTree.SubElement(el, 'link', {
            'rel': 'alternate',
            'type': 'text/html',
            'href': uri,
        })

        child_el = ElementTree.SubElement(el, 'content', {'type': 'html',})
        child_el.text = render(self.content_template, {'entry': entry,})
