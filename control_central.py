#!/usr/bin/env python

from __future__ import print_function

from eccontrols import *
from eccontrols import generic
from eccontrols import pioneer

import collections
import copy
import time
import threading

class ControlCentral:
    """Manages the organized control of all components in my entertainment center."""

    _devices = {
        'Receiver': generic.GenericIR('YamahaRXV683'),
        'DVR': generic.GenericIR('X1'),
        'Blu-Ray': generic.GenericIR('SonyBluRay'),
        'TV': generic.GenericIR('SonyTV'),
        'pause': time.sleep,
       }

    _modes = collections.OrderedDict([
            ('Everything Off', [
		    ('Receiver', 'INPUT-HDMI-2'),
                    ('Receiver', 'POWER-OFF'),
                    ('TV', 'POWER-OFF'),
                    ('Blu-Ray', 'POWER-OFF'),
                    ]),
            ('TV', [
                    ('Receiver', 'POWER-ON'),
                    ('TV', 'POWER-ON'),
                    ('pause', 1),
                    ('Receiver', 'INPUT-HDMI-2'),
                    ]),
            ('Blu-Ray', [
                    ('Receiver', 'POWER-ON'),
                    ('TV', 'POWER-ON'),
                    ('Blu-Ray', 'POWER-ON'),
                    ('pause', 1),
                    ('Receiver', 'INPUT-HDMI-1'),
                    ]),
            ('Fire TV', [
                    ('Receiver', 'POWER-ON'),
                    ('TV', 'POWER-ON'),
                    ('pause', 1),
                    ('Receiver', 'INPUT-HDMI-5'),
                    ]),
            ('Chromecast', [
                    ('Receiver', 'POWER-ON'),
                    ('TV', 'POWER-ON'),
                    ('pause', 1),
                    ('Receiver', 'INPUT-HDMI-4'),
                    ]),
            ('Switch-PS-XBox', [
                    ('Receiver', 'POWER-ON'),
                    ('TV', 'POWER-ON'),
                    ('pause', 1),
                    ('Receiver', 'INPUT-HDMI-3'),
                    ]),
            ('Playstation 2', [
                    ('Receiver', 'POWER-ON'),
                    ('TV', 'POWER-ON'),
                    ('pause', 1),
                    ('Receiver', 'INPUT-AV-2'),
                    ]),
            ])

    _currentMode = None
    _mute = None

    def __init__(self):
        self._currentMode = 'Everything Off'
        self._mute = Switch.off

    def send(self, device, code):
        if not device in self._devices:
            raise ECError('No such device ' + device)
        self._devices[device](code)

    def sendSequence(self, sequence):
        for device, code in sequence:
            self.send(device, code)

    def getModes(self):
        return self._modes.keys()

    def getCurrentMode(self):
        return self._currentMode

    def getMute(self):
        return self._mute

    def mute(self, flag):
        if flag == Switch.toggle:
            flag = ToggleSwitch(self.getMute())

        if flag == Switch.off:
            self.send('Receiver', 'mute-off')
        elif flag == Switch.on:
            self.send('Receiver', 'mute-on')
        else:
            raise ECError('No such switch flag for power: %s' % flag)
        self._mute = flag

    def volume_down(self, value):
        for i in range(value):
            self.send('Receiver', 'volume-down')

    def volume_up(self, value):
        for i in range(value):
            self.send('Receiver', 'volume-up')

    def changeMode(self, mode):
        if not mode in self._modes:
            raise ECError('No such mode: %s' % flag)
        self.sendSequence(self._modes[mode])
        self._currentMode = mode

    def cycleReceiverPower(self):
        self.send('Receiver', 'power-off')
        self.send('pause', 5)
        self.send('Receiver', 'power-on')

if __name__ == '__main__':
    control = ControlCentral()
    control.sendSequence([('Receiver', 'volume-down'), ('Receiver', 'volume-down')])
