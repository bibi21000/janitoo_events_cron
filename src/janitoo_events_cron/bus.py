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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger(__name__)
import os
import time
from random import randint

from apscheduler.schedulers.background import BackgroundScheduler

from janitoo.bus import JNTBus
from janitoo.thread import JNTBusThread
from janitoo.value import JNTValue
from janitoo.options import get_option_autostart

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_METER = 0x0032
COMMAND_CONFIGURATION = 0x0070
COMMAND_METER = 0x0032
COMMAND_EVENT_ACTIVATION = 0x1010
COMMAND_EVENT_ACTUATOR_CONF = 0x1011
COMMAND_EVENT_CONTROLLER_CONF = 0x1012

assert(COMMAND_DESC[COMMAND_METER] == 'COMMAND_METER')
assert(COMMAND_DESC[COMMAND_METER] == 'COMMAND_METER')
assert(COMMAND_DESC[COMMAND_EVENT_ACTIVATION] == 'COMMAND_EVENT_ACTIVATION')
assert(COMMAND_DESC[COMMAND_EVENT_ACTUATOR_CONF] == 'COMMAND_EVENT_ACTUATOR_CONF')
assert(COMMAND_DESC[COMMAND_EVENT_CONTROLLER_CONF] == 'COMMAND_EVENT_CONTROLLER_CONF')
assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
##############################################################

def extend( self ):

    self.events_crons = None
    self.export_attrs('events_crons', self.events_crons)

    self._events_crons_start = self.start
    def start(mqttc, trigger_thread_reload_cb=None):
        """Start the bus"""
        logger.debug("[%s] - Start the bus %s", self.__class__.__name__, self.oid )
        self.events_crons = BackgroundScheduler()
        self.events_crons.start()
        self.update_attrs('events_crons', self.events_crons)
        return self._events_crons_start(mqttc, trigger_thread_reload_cb=trigger_thread_reload_cb)
    self.start = start

    self._events_crons_stop = self.stop
    def stop():
        """Stop the bus"""
        if self.events_crons is not None:
            self.events_crons.shutdown()
        ret = self._events_crons_stop()
        self.events_crons = None
        self.update_attrs('events_crons', self.events_crons)
        return ret
    self.stop=stop

