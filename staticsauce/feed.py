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


import datetime
import StringIO
import xml.etree.ElementTree as etree


class Feed(object):
    def __init__(self):
        self.title = None
        self.authors = []
        self.updated = datetime.datetime.now()
        self.id = None
        self.entries = []

    def element(self):
        feed = etree.Element('feed')

        title = etree.SubElement(feed, 'title')
        title.text = self.title

        for author in self.authors:
            feed.append(author.element())

        id = etree.SubElement(feed, 'id')
        id.text = self.id

        for entry in self.entries:
            feed.append(entry.element())

        return feed

    def xml(self):
        return etree.tostring(self.element(), encoding="UTF-8")


class Author(object):
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

    def element(self):
        author = etree.Element('author')
        name = etree.SubElement(author, 'name')
        name.text = self.name
        if self.email:
            email = etree.SubElement(author, 'email')
            email.text = self.email
        return author


class Entry(object):
    def __init__(self, content):
        self.title = None
        self.updated = None
        self.content = content

    def element(self):
        entry = etree.Element('entry')
        title = etree.SubElement(entry, 'title')
        title.text = self.title
        content = etree.SubElement(entry, 'content', {'type': 'html'})
        content.text = self.content
        return entry
