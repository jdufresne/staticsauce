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
from PIL import Image
from staticsauce import templating


class StaticFile(object):
    def save(self, filename):
        raise NotImplementedError


class TemplateFile(StaticFile):
    def __init__(self, template, context):
        super(TemplateFile, self).__init__()
        self.template = template
        self.context = context

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(templating.render(self.template, self.context))

    def src_mtime(self):
        return os.stat(templating.filename(self.template)).st_mtime


class JPEGFile(StaticFile):
    def __init__(self, src_filename, size, quality, crop=False):
        super(JPEGFile, self).__init__()
        self.src_filename = src_filename
        self.size = size
        self.crop = crop
        self.quality = quality

    def src_mtime(self):
        return os.stat(self.src_filename).st_mtime

    def save(self, dest_filename):
        self.preprocess_image().save(
            dest_filename,
            'JPEG',
            quality=self.quality
        )

    def preprocess_image(self):
        image = Image.open(self.src_filename)
        scaled_image = self.resize(image)
        if self.crop:
            scaled_image = self.crop_center(scaled_image)
        return scaled_image

    def resize(self, image):
        if not self.crop and image.size[0] >= image.size[1] or \
                not not self.crop and image.size[1] >= image.size[0]:
            width = self.size[0]
            height = width * image.size[1] / image.size[0]
        else:
            height = self.size[1]
            width = height * image.size[0] / image.size[1]
        return image.resize((width, height), Image.ANTIALIAS)

    def crop_center(self, image):
        left = (image.size[0] - self.size[0]) / 2 \
            if image.size[0] > self.size[0] else 0
        top = (image.size[1] - self.size[1]) / 2 \
            if image.size[1] > self.size[1] else 0
        box = left, top, left + self.size[0], top + self.size[1]
        return image.crop(box)
