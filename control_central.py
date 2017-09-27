#!/usr/bin/env python

from eccontrols import *
from eccontrols import generic
from eccontrols import pioneer

import copy
import time
import threading

class ControlCentral:
    """Manages the organized control of all components in my entertainment center."""

    # If you add a new device, also add to the receiver list.
    devices = [
        'Everything Off',
        'DirecTV',
        'Blu-Ray',
        'Chromecast',
        'PS4',
        'XBox 360',
        'Wii',
        'Playstation 2' ]
            

    _bluray = None
    _receiver = None
    _directv = None
    _tv = None

    def _queryReceiver(self):
        self._receiver.querySocket()
        threading.Timer(300, self._queryReceiver).start()

    def __init__(self):
        self._bluray = generic.GenericIR('SonyBluRay')
        self._receiver = pioneer.ReceiverIR()
        self._directv = generic.GenericIR('DirecTV')
        self._tv = generic.GenericIR('SonyTV')
        self._queryReceiver()

    def getCurrentState(self):
        if self._receiver.getPower() == Switch.off:
            return 'Everything Off'
        else: # Power is on
            deviceName  = self._receiver.getInput()
            if deviceName in self.devices:
                return deviceName
            else:
                return 'Everything Off'

    def getVolume(self):
        return self._receiver.getVolume()

    def getMute(self):
        return self._receiver.getMute()

    def mute(self, flag):
        self._receiver.mute(flag)

    def volume(self, level):
        self._receiver.volume(level)

    def changeMode(self, mode):
        if mode == 'Everything Off':
            self._tv.send('power-off')
            self._receiver.power(Switch.off)
            self._bluray.send('power-off')
        else:
            self._tv.send('power-on')
            self._receiver.power(Switch.on)
            time.sleep(1)
            self._receiver.input(mode)
            if mode == 'Blu-Ray':
                self._bluray.send('power-on')
            #TODO set up other devices

    def sendReceiver(self, command):
        self._receiver.send(command)

    def sendDirecTV(self, command):
        self._directv.send(command)

    def sendTV(self, command):
        self._tv.send(command)

    def sendBluRay(self, command):
        self._bluray.send(command)

if __name__ == '__main__':
    control = ControlCentral()
    print control.devices.index(control.getCurrentState())
    print control.getVolume()
    print control.getMute()
