# Tangibl.me - federated marketplace based on GNU Mediagoblin
# Copyright (C) 2014 Metamaquina.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Inspired by mediagoblin.tools.licenses
# Yes, this is dirty... use the database and let users input their stuff?

from collections import namedtuple, OrderedDict

Color = namedtuple("Color", ["name", "hexcode"])
Delivery = namedtuple("Delivery", ["name", "desc")
Material = namedtuple("Material", ["name", "desc"])
Model = namedtuple("Model", ["name", "thumb"])


#TODO: put values in csv file
__COLORS = OrderedDict(
  sorted(({
    'red'  : Color("Red", "FF0000"),
    'green': Color("Green", "00FF00"),
    'blue' : Color("Blue", "0000FF")
  }).items(), key = lambda t: t[1].name))

#TODO: put values in csv file
__DELIVERY = OrderedDict(
  {
    'pickup'  : Delivery("Pickup", "Buyer picks up part at bureau"),
    'postal'  : Delivery("Postal service", "Part delivered by postal service"),
    'deliver' : Delivery("Delivery", "Bureau delivers part to buyer")
  })

#TODO: put values in csv file
__MATERIALS = OrderedDict(
  {
    'abs': Material("ABS", "Acrylonitrile butadiene styrene"),
    'pla': Material("PLA", "Polylactic acid"),
    'nyl': Material("Nylon", "Nylon"),
    'pva': Material("PVA", "Polyvinyl acetate"),
    'hip': Material("HIPS", "High impact polystyrene"),
    'pc' : Material("PC", "Polycarbonate"),
    'oth': Material("Other", "Other material (see printer description)")
  })

#TODO: put values in csv file
__MODELS = OrderedDict(
  {
    'cupcake': Model("MakerBot Cupcake CNC", "images/flaticon_cupcake.svg"),
    'mm2'    : Model("Metamaquina 2", "images/flaticon_mm2.svg"),
    'other'  : Model("Other", "images/flaticon_3dprinter.svg"

def get_color(code):
    """Look up a color by its code and return the Color object"""
    try:
        return __COLORS[code]
    except KeyError:
        # in case of an unknown color, just display something
        # rather than exploding in the user's face.
        return Color('Unknown color ' + code, '000000')

def color_choices():
    """
    List of (name, hexcode) color tuples for HTML choice field population
    """
    return [(c[0], c[1].name) for c in __COLORS.items()]

def get_delivery(code):
    """Look up a delivery by its code and return the Delivery object"""
    try:
        return __DELIVERY[code]
    except KeyError:
        # in case of an unknown color, just display something
        # rather than exploding in the user's face.
        return Delivery(code, code)

def delivery_choices():
    """
    List of (name, hexcode) color tuples for HTML choice field population
    """
    return [(d[0], d[1].name) for c in __DELIVERY.items()]

def get_material(code):
    """Look up a material by its code and return the Material object"""
    try:
        return __MATERIALS[code]
    except KeyError:
        # in case of an unknown material, just display something
        # rather than exploding in the user's face.
        return Material(code, 'Unknown material ' + code)

def material_choices():
    """
    List of (name, desc) material tuples for HTML choice field population
    """
    return [(m[0], m[1].name) for m in __MATERIALS.items()]
