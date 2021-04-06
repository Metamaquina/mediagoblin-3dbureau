# GNU MediaGoblin -- federated, autonomous media hosting
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

MIGRATIONS = {}

import datetime
import uuid

from sqlalchemy import (MetaData, Table, Column, Boolean, SmallInteger,
                        Integer, Unicode, UnicodeText, DateTime,
                        ForeignKey, Date, Float)
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_
from migrate.changeset.constraint import UniqueConstraint

from mediagoblin.db.extratypes import JSONEncoded, MutationDict
from mediagoblin.db.migration_tools import (
    RegisterMigration, inspect_table, replace_table_hack)
from mediagoblin.db.models import (MediaEntry, Collection, MediaComment, User, 
        Privilege)
from mediagoblin.db.extratypes import JSONEncoded, MutationDict


class Bureau_v0(declarative_base()):
    __tablename__ = "3dbureau__bureau"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(User.id), nullable=False)

class Printer_v0(declarative_base()):
    __tablename__ = "3dbureau__printer"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    model = Column(Unicode, nullable=False)
    bureau_id = Column(Integer, ForeignKey('3dbureau__bureau.id'), nullable=False)
    active_since = Column(DateTime, nullable=False, default=datetime.datetime.now)
    setup_fee = Column(Float)
    volume_fee = Column(Float) 

"""
class CollectionItem_v0(declarative_base()):
    __tablename__ = "core__collection_items"

    id = Column(Integer, primary_key=True)
    media_entry = Column(
        Integer, ForeignKey(MediaEntry.id), nullable=False, index=True)
    collection = Column(Integer, ForeignKey(Collection.id), nullable=False)
    note = Column(UnicodeText, nullable=True)
    added = Column(DateTime, nullable=False, default=datetime.datetime.now)
    position = Column(Integer)

    ## This should be activated, normally.
    ## But this would change the way the next migration used to work.
    ## So it's commented for now.
    __table_args__ = (
        UniqueConstraint('collection', 'media_entry'),
        {})

collectionitem_unique_constraint_done = False
"""
@RegisterMigration(1, MIGRATIONS)
def add_bureau_tables(db_conn):
    Bureau_v0.__table__.create(db_conn.bind)
    Printer_v0.__table__.create(db_conn.bind)
    db_conn.commit()
