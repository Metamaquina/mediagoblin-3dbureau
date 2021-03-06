# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2014, Metamaquina.  See AUTHORS.
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


import wtforms

from mediagoblin.tools.translate import lazy_pass_to_ugettext as _

class AddPrinterForm(wtforms.Form):
    name = wtforms.TextField(
        _('Name'),
        [wtforms.validators.Length(min=0, max=50), wtforms.validators.Required()])
    model = wtforms.TextAreaField(
        _('Model'),
        [wtforms.validators.Length(min=0, max=500), wtforms.validators.Required()],
        description=_("""Choose your printer model"""))
