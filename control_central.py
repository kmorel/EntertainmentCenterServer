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
        'Fire TV',
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
        self._receiver = pioneer.ReceiverSocket()
        self._directv = generic.GenericIR('DirecTV', duration=1)
        self._tv = generic.GenericIR('SonyTV')
        # Disabling because this is not working right now and current setup is
        # not fully queryable.
        #self._queryReceiver()

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
            # I used to power off the receiver. However, often we use the DirecTV
            # remote directly, and that does not turn the receiver on/off.
            # Instead, leave the receiver on but switch it to DirecTV mode.
            #self._receiver.power(Switch.off)
            self._receiver.input('DirecTV')
            self._directv.send('power-off')
            self._bluray.send('power-off')
        else:
            self._tv.send('power-on')
            if mode == 'DirecTV':
                self._directv.send('power-on')
            elif mode == 'Blu-Ray':
                self._bluray.send('power-on')
            #TODO set up other devices
            self._receiver.power(Switch.on)
            time.sleep(1)
            self._receiver.input(mode)

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
