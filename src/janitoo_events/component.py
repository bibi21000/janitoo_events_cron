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
try:  # Python 2.7+                                   # pragma: no cover
    from logging import NullHandler                   # pragma: no cover
except ImportError:                                   # pragma: no cover
    class NullHandler(logging.Handler):               # pragma: no cover
        """NullHandler logger for python 2.6"""       # pragma: no cover
        def emit(self, record):                       # pragma: no cover
            pass                                      # pragma: no cover
logger = logging.getLogger("janitoo.buses.onewire")
from janitoo.bus import JNTBus
from janitoo.value import JNTValue, value_config_poll
from janitoo.node import JNTNode
from janitoo.component import JNTComponent
import os
import time

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_METER = 0x0032
COMMAND_CONFIGURATION = 0x0070

assert(COMMAND_DESC[COMMAND_METER] == 'COMMAND_METER')
assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
##############################################################

def make_component(**kwargs):
    return DawnDusk(**kwargs)

class DawnDusk(JNTComponent):
    """ Provides the interface for a DS18B20 device. """

    def __init__(self, bus=None, addr=None, lock=None, unit="°C", **kwargs):
        """ Constructor.

        Arguments:
            bus:
                a 1-Wire instance representing the bus this device is
                connected to
            addr:
                the 1-Wire device address (in 7 bits format)
        """
        JNTComponent.__init__(self, 'onewire.ds18b20', bus=bus, addr=addr, name="DS18B20 range sensor", **kwargs)
        uuid = '%s_%s'%('ds18b20','c')
        value = JNTValue( uuid=uuid,
                help='The temperature',
                label='Temp',
                units='°C',
                index=0,
                cmd_class=COMMAND_METER,
                genre=0x02,
                type=0x03,
                get_data_cb=self.read_temp_c,
                is_writeonly=False,
                is_polled=True,
                poll_delay=300,
                )
        self.values[uuid] = value
        uuid = '%s_%s'%('ds18b20','c_poll')
        value = value_config_poll( uuid, self.poll_tempc_get, self.poll_tempc_set)
        self.values[uuid] = value
        uuid = '%s_%s'%('ds18b20','f')
        value = JNTValue( uuid=uuid,
                help='The temperature',
                label='Temp',
                units='°F',
                index=0,
                cmd_class=COMMAND_METER,
                genre=0x02,
                type=0x03,
                get_data_cb=self.read_temp_f,
                is_writeonly=False,
                is_polled=False,
                poll_delay=300,
                )
        self.values[uuid] = value
        uuid = '%s_%s'%('ds18b20','f_poll')
        value = value_config_poll( uuid, self.poll_tempf_get, self.poll_tempf_set, default=0)
        self.values[uuid] = value
        self.cmd_classes.append(COMMAND_METER)
        self.cmd_classes.append(COMMAND_CONFIGURATION)

    def read_temp_raw(self):
        """
        """
        lines = None
        try:
            f = open(os.path.join(self._bus.bus_path, self._addr, 'w1_slave'), 'r')
            lines = f.readlines()
            f.close()
        except:
            logger.exception('Exception when reading temperature')
        return lines

    def read_temp_c(self, node_uuid, index):
        """
        """
        lines = self.read_temp_raw()
        if lines is None:
            return None
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def read_temp_f(self, node_uuid, index):
        """
        """
        temp_c = self.read_temp_c(node_uuid, index)
        if temp_c is None:
            return None
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

    def poll_tempf_get(self, node_uuid, index):
        """
        """
        return self.value_poll_get(node_uuid, index, '%s_%s'%('ds18b20','f'))

    def poll_tempf_set(self, node_uuid, index, value):
        """
        """
        self.value_poll_set(node_uuid, index, value, '%s_%s'%('ds18b20','f'))

    def poll_tempc_get(self, node_uuid, index):
        """
        """
        return self.value_poll_get(node_uuid, index,'%s_%s'%('ds18b20','c'))

    def poll_tempc_set(self, node_uuid, index, value):
        """
        """
        self.value_poll_set(node_uuid, index, value, '%s_%s'%('ds18b20','c'))
