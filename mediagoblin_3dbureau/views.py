# GNU MediaGoblin -_ federated, autonomous media hosting
# Copyright (C) 2013 MediaGoblin contributors.  See AUTHORS.
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

import logging

from mediagoblin import mg_globals
from mediagoblin.db.models import User
from mediagoblin.decorators import (require_active_login, active_user_from_url,
                                    uses_pagination)
from mediagoblin.messages import add_message, SUCCESS, ERROR
from mediagoblin.tools.pagination import Pagination
from mediagoblin.tools.response import render_to_response, redirect
from mediagoblin.tools.translate import pass_to_ugettext as _

from mediagoblin_3dbureau.models import Bureau, Printer
from mediagoblin_3dbureau.forms import AddPrinterForm


_log = logging.getLogger(__name__)

@active_user_from_url
@require_active_login
@uses_pagination
def list_printers(request, url_user, page, **kwargs):
    """Just testing..."""

    # url_user is the bureau owner
    # TODO put bureau activation somewhere else!
    print url_user
    user = request.db.User.query.get(url_user.id)
    if not user.bureau:
        bureau = request.db.Bureau(owner = url_user)
        bureau.save()
        user.bureau = bureau
        _log.info("Created new bureau: " + repr(user.bureau))
        #TODO: redirect user to agreement when bureau activated
    else:
        _log.info("Existing bureau: " + repr(user.bureau))

    cursor = Printer.query.filter_by(bureau_id = user.bureau.id
                                     ).order_by(Printer.active_since.desc())

    pagination = Pagination(page, cursor)
    printer_entries = pagination()

    return render_to_response(
        request,
        'mediagoblin/plugins/3dbureau/list_printers.html',
        {'user': url_user,
         'bureau': user.bureau,
         'printer_entries': printer_entries,
         'pagination': pagination
         })

@require_active_login
def submit_printer(request):
    """
    View to create a new printer
    """
    submit_form = AddPrinterForm(request.form)

    if request.method == 'POST' and submit_form.validate():
        printer = request.db.Printer()

        printer.name = unicode(submit_form.name.data)
        printer.model = unicode(submit_form.model.data)
        printer.bureau = request.user.bureau

        # Make sure this user isn't duplicating an existing printer
        existing_printer = request.db.Printer.query.filter_by(
                bureau_id=printer.bureau.id,
                name=printer.name).first()

        _log.info("Existing printer: " + repr(existing_printer))

        if existing_printer:
            add_message(request, ERROR,
                _('You already have a printer called "%s"!') \
                    % printer.name)
        else:
            printer.save()

            add_message(request, SUCCESS,
                _('Printer "%s" added!') % printer.name)

        return redirect(request, "mediagoblin_3dbureau.list_printers",
                        user=request.user.username)

    return render_to_response(
        request,
        'mediagoblin/plugins/3dbureau/submit_printer.html',
        {'submit_form': submit_form,
         'app_config': mg_globals.app_config})
