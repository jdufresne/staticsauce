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


import argparse
import glob
import inspect
import os
from staticsauce import commands

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    commands_dir = os.path.join(os.path.dirname(commands.__file__))

    for filename in glob.iglob(os.path.join(commands_dir, '*.py')):
        filename = os.path.basename(filename)
        module_name, ext = os.path.splitext(filename)

        module_components = ['staticsauce', 'commands', module_name]
        module = __import__('.'.join(module_components))
        for component in module_components[1:]:
            module = getattr(module, component)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, commands.Command):
                command = obj()
                subparser = subparsers.add_parser(command.command)
                command.init_parser(subparser)
                subparser.set_defaults(_command=command)

    args = parser.parse_args()
    kwargs = {name: obj for name, obj in inspect.getmembers(args)
              if not name.startswith('_')}
    command = args._command
    command.precommand(**kwargs)
    command(**kwargs)
