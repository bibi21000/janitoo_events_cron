# -*- coding: utf-8 -*-
"""The 1-wire Bus
It handle all communications to the onewire bus

"""

__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger(__name__)
import os
import time
from janitoo.bus import JNTBus
from janitoo.value import JNTValue, value_config_poll
from janitoo.node import JNTNode
from janitoo.component import JNTComponent
from janitoo_events.thread import OID

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_METER = 0x0032
COMMAND_CONFIGURATION = 0x0070

assert(COMMAND_DESC[COMMAND_METER] == 'COMMAND_METER')
assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
##############################################################

def make_weekly(**kwargs):
    return Weekly(**kwargs)

class Weekly(JNTComponent):
    """ Provides """

    def __init__(self, bus=None, addr=None, lock=None, unit="°C", **kwargs):
        """ Constructor.

        """
        JNTComponent.__init__(self, '%s.weekly'%OID, bus=bus, addr=addr, name="Weekly cron", **kwargs)
