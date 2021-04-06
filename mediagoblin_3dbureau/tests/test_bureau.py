
# GNU MediaGoblin -- federated, autonomous media hoppsting
# Copyright (C) 2011, 2012, 2013, 2014 MediaGoblin contributors.  See AUTHORS.
# Copyright (C) 2014 Metamaquina. See AUTHORS.
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

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import pytest

try:
    import mediagoblin
except ImportError:
    raise ImportError("The mediagoblin_3dbureau plugin tests require an installed mediagoblin package")

from mediagoblin import mg_globals
from mediagoblin.db.base import Session
from mediagoblin.db.models import User
from mediagoblin.init.plugins import setup_plugins
from mediagoblin.tests import MGClientTestCase
from mediagoblin.tests.tools import fixture_add_user

import mediagoblin_3dbureau
from mediagoblin_3dbureau.models import *

def fixture_add_bureau(user):
    test_bureau = Bureau(owner = user)
    test_bureau.save()
    id = test_bureau.id
    # Reload
    test_bureau = Bureau.query.filter_by(id=id).first()
    return test_bureau

class Test3DBureauDB:
    @pytest.fixture(autouse=True)
    def setup(self, test_app):
        fixture_add_user()
        self.user = User.query.filter_by(username=u'chris').first()
        setup_plugins()
        self.bureau = None

    def test_add_bureau(self, test_app):
        self.bureau = fixture_add_bureau(self.user)
        assert self.bureau
        assert self.bureau.owner == self.user
        assert self.user.bureau == self.bureau
        assert self.bureau.active_since <= datetime.datetime.utcnow()
        self.user = User.query.filter_by(username=u'chris').first()
        assert self.user.bureau

    def test_add_printer(self, test_app):
        user = User.query.filter_by(username=u'chris').first()
        bureau = fixture_add_bureau(user)
        id = bureau.id
        bureau.save()
        bureau = Bureau.query.get(id)
        gatinho = Printer(name=u'Gatinho de Beco', model=u'Metamaquina 2')
        gatinho.bureau = bureau
        gatinho.save
        minha = Printer(name=u'Minha Metamaquina', model=u'Metamaquina 3D')
        minha.bureau = bureau
        minha.save()
        # fetch again
        bureau = Bureau.query.get(id)
        print bureau.printers
        assert bureau.printer_count() == 2

    def test_remove_printer(self, test_app):
        pass

    def test_remove_user(self, test_app):
        pass

    def test_remove_user(self, test_app):
        pass
