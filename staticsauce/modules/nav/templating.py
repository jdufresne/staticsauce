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


from staticsauce.templating import inclusiontag
from staticsauce.modules.nav.models import menus


def context_processor():
    return {
        'menus': menus(),
        'nav': nav,
    }


# @contextfunction
# def active_menu_item(ctx, menu, item):
#    return ''


@inclusiontag('/nav/nav.html')
def nav(menu, active):
    return {
        'menu': menu,
        'active': active,
    }
