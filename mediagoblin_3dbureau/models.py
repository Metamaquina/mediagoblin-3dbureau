# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# 3DBureau - plugin for distributed 3D Printing Service Bureaus
# Copyright (C) 2014 Metamaquina
# Written by Rodrigo Rodrigues da Silva <rsilva@metamaquina.com.br>
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

import datetime

from sqlalchemy import (
    Column, Integer, Float, Unicode, DateTime, ForeignKey)
from sqlalchemy.orm import relationship, backref

from mediagoblin import mg_globals
from mediagoblin.db.base import Base
from mediagoblin.init import get_staticdirector
#from mediagoblin.db.models import MediaEntry

from mediagoblin_3dbureau import util

class Bureau(Base): #TODO: inherit from User: Bureau(User)
    __tablename__ = "3dbureau__bureaus"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    desc = Column(Unicode)
    owner_id = Column(Integer, ForeignKey('core__users.id'), nullable=False)
    owner = relationship("User", backref=backref('bureau', uselist=False))
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    active = Column(Boolean, nullalbe=False, default=True)
    location = Column(Unicode, nullable=False)
    invoicing = Column(Boolean, nullable=False, default=False)
    _delivery = Column(Integer, nullable=False)

    @property
    def delivery(self):
        return util.get_delivery(self._delivery)

    def printer_count(self):
        return len(self.printers)

    def __repr__(self):
        return "<Bureau #{id}: by #{uid} {user}>".format(
            id=self.id,
            uid=self.owner.id,
            user=self.owner.username
        )

class Printer(Base):
    __tablename__ = "3dbureau__printers"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    _model = Column(String, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    active = Column(Boolean, nullalbe=False, default=False)
    setup_fee = Column(Float, nullable=False)
    volume_fee = Column(Float, nullable=False)
    delivery_days = Column(Integer, nullable=False, default=3)

    bureau_id = Column(Integer, ForeignKey('3dbureau__bureau.id'), nullable=False)
    bureau = relationship(Bureau,
                          backref=backref('printers', uselist=True, cascade='delete,all'))

    @property
    def model(self):
        return util.get_model(self._model)

    # HACK: make Printer() compatible with object_gallery
    @property
    def title(self):
        return self.name

    # HACK: make Printer() compatible with object_gallery
    @property
    def thumb_url(self):
        # TODO get thumb from 3DPrinter_Model or from user pic
        # see mixin.py MediaEntry
        return mg_globals.app.staticdirector("images/flaticon_3dprinter.svg", 
                                             'mediagoblin_3dbureau')

    # HACK: make Printer() compatible with object_gallery    
    def url_for_self(self, urlgen, **extra_args):
        # TODO: figure out what to do with it
        return ""

    def __repr__(self):
        return "<3DPrinter #{id}: {name} from #{bid}>".format(
            id=self.id,
            name=self.name.encode("utf-8"),
            bid=self.bureau.id
        )

class PrinterSetup(Base):
    __tablename__ = "3dbureau__printer_setups"
    id = Column(Integer, primary_key=True)
    _color = Column(String, nullable = False)
    _material = Column(String, nullable = False)
    volume_fee = Column(Float)

    printer_id = Column(Integer, ForeignKey(Printer.id), nullable=False)
    printer = relationship(Printer,
              backref=backref('printer_setups', uselist=True, cascade='delete,all'))

    @property
    def color(self):
        return util.get_color(self._color)

    @property
    def material(self):
        return util.get_model(self._material)

    def __repr__(self):
        return "<PrinterSetup #{id}: {color} {material} from #{pid}>".format(
            id=self.id,
            color=self.color.name,
            material=self.material.name,
            pid=self.printer.id
        )


MODELS = [Printer, Bureau, PrinterSetup]
