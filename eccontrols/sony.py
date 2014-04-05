#!/usr/bin/env python

from eccontrols import *

from lirc import lirc

class TV:
    """Controls a Sony TV through the IR interface."""

    codes = {
        'power-on': 'POWER_ON',
        'power-off': 'POWER_OFF'
        }

    def ircode(self, code):
        """Send the IR code. The codes are defined in the codes field."""
        if code.lower() in self.codes:
            lirc.send('SonyTV', self.codes[code.lower()])
        else:
            print 'No such code: %s' % code

