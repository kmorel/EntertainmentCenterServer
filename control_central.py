#!/usr/bin/env python

from eccontrols import *
from eccontrols import pioneer
from eccontrols import tivo

import copy
import time

class ControlCentral:
    """Manages the organized control of all components in my entertainment center."""

    # If you add a new device, also added to the receiver list.
    devices = [
        'TiVo',
        'Blu-Ray',
        'XBox 360',
        'Wii',
        'Playstation 2',
        'Turn Everything Off' ]
            

    _receiver = None
    _tivo = None

    def __init__(self):
        self._receiver = pioneer.Receiver()
        self._tivo = tivo.TiVo()

    def getCurrentState(self):
        if self._receiver.getPower() == Switch.off:
            return 'Turn Everything Off'
        else: # Power is off
            deviceName  = self._receiver.getInput()
            if deviceName in self.devices:
                return deviceName
            else:
                return 'Turn Everything Off'

    def getVolume(self):
        return self._receiver.getVolume()

    def getMute(self):
        return self._receiver.getMute()

    def mute(self, flag):
        self._receiver.mute(flag)

    def volume(self, level):
        self._receiver.volume(level)

    def changeMode(self, mode):
        if mode == 'Turn Everything Off':
            self._receiver.power(Switch.off)
        else:
            self._receiver.power(Switch.on)
            time.sleep(1)
            self._receiver.input(mode)
            #TODO set up other devices

    def sendTiVo(self, ircode):
        self._tivo.ircode(ircode)

    def sendTiVoSecondsBack(self, t):
        self._tivo.secondsBack(t)

    def sendTiVoSecondsForward(self, t):
        self._tivo.secondsForward(t)

    def gotoTiVoScreen(self, screen):
        self._tivo.teleport(screen)

if __name__ == '__main__':
    control = ControlCentral()
    print control.devices.index(control.getCurrentState())
    print control.getVolume()
    print control.getMute()
