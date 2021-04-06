# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2014 Kevin Brubeck Unhammer & contributors.
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


import logging, os
from pkg_resources import resource_filename

from mediagoblin.tools import pluginapi
from mediagoblin.tools.staticdirect import PluginStatic

PLUGIN_DIR = os.path.dirname(__file__)
_log = logging.getLogger(__name__)
_setup_plugin_called = 0

def setup_plugin():
    global _setup_plugin_called

    _log.info('3DBureau plugin setup started!')
    config = pluginapi.get_config('mediagoblin.plugins.3dbureau')
    if config:
        _log.info('%r' % config)
    else:
        _log.info('There is no configuration set.')
    _setup_plugin_called += 1

    routes = [
        ('mediagoblin_3dbureau.list_printers',
         '/u/<string:user>/printers',
         'mediagoblin_3dbureau.views:list_printers'),
        ('mediagoblin_3dbureau.submit_printer',
         '/submit/printer',
         'mediagoblin_3dbureau.views:submit_printer')
        ]

    pluginapi.register_routes(routes)

    pluginapi.register_template_path(os.path.join(PLUGIN_DIR, 'templates'))
    pluginapi.register_template_hooks({
        "user_profile": "mediagoblin/plugins/3dbureau/browse_3dprinters_link.html",
#        "pre_header_right": "mediagoblin/plugins/3dbureau/foo.html",
     })

    _log.info('3DBureau plugin setup done!')

def setup_static():
    return PluginStatic('mediagoblin_3dbureau',
        resource_filename('mediagoblin_3dbureau', 'static'))

hooks = {
    'setup': setup_plugin,
    'static_setup': setup_static
    }
