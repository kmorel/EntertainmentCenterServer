#!/usr/bin/env python

from eccontrols import *

import socket
import time

class Receiver:
    """Controls a Pioneer receiver through a web interface."""
    hostname = 'vsx-60.local'
    port = 23

    _connection = None

    _power = None
    _volume = None
    _mute = None
    _input = None

    # Would be better off in configuration
    inputs = {
        'TiVo': 06,
        'Playstation 2': 15,
        'XBox 360': 24,
        'Blu-Ray': 25,
        'Wii': 04
        }

    def _getStatus(self):
        gotData = False
        while True:
            try:
                data = self._connection.recv(1024).split()
                gotData = True
                for status in data:
                    print status
                    if status.startswith('PWR'):
                        if status[3] == '0':
                            self._power = Switch.on
                        elif status[3] == '1':
                            self._power = Switch.off
                        else:
                            print 'Unknown power:', status[3:]
                    elif status.startswith('VOL'):
                        self._volume = int(status[3:])
                    elif status.startswith('MUT'):
                        if status[3] == '0':
                            self._mute = Switch.on
                        elif status[3] == '1':
                            self._mute = Switch.off
                        else:
                            print 'Unknown power:', status[3:]
                    elif status.startswith('FN'):
                        self._input = int(status[2:])
            except socket.error:
                break;
        return gotData

    def _sendCommand(self, command, waitForResponse=False):
        self._getStatus()
        self._connection.send(command + '\r\n')
        if waitForResponse:
            while True:
                if self._getStatus():
                    break

    def __init__(self):
        while not self._connection:
            try:
                self._connection = socket.create_connection((self.hostname,self.port))
            except socket.gaierror:
                print 'Bad connection. Trying again.'
        self._connection.setblocking(0)
        self._sendCommand('')
        time.sleep(0.1)
        self._getStatus()

    def getPower(self):
        self._sendCommand('?P', True)
        return self._power

    def power(self, flag=Switch.toggle):
        if flag == Switch.off:
            self._sendCommand('PF')
        elif flag == Switch.on:
            self._sendCommand('PO')
        elif flag == Switch.toggle:
            if self.getPower() == Switch.on:
                self.power(Switch.off)
            else:
                self.power(Switch.on)
        else:
            raise Exception('No such switch flag for power: %s' % flag)

    def getVolume(self):
        self._sendCommand('?V', True)
        return self._volume

    def volume(self, value):
        """Set the volume. The volume is an integer in the range 0 to 185 where
0 is no volume, 1 is -80 dB, 161 is 0 dB, and 185 is +12 dB"""
        self._sendCommand('%03dVL' % value)

    def getMute(self):
        self._sendCommand('?M', True)
        return self._mute

    def mute(self, flag=Switch.toggle):
        if flag == Switch.off:
            self._sendCommand('MF')
        elif flag == Switch.on:
            self._sendCommand('MO')
        elif flag == Switch.toggle:
            if self.getMute() == Switch.on:
                self.mute(Switch.off)
            else:
                self.mute(Switch.on)
        else:
            raise Exception('No such switch flag for power: %s' % flag)

    def getInput(self):
        self._sendCommand('?F', True)
        # Find name, if available
        for name, index in self.inputs.items():
            if index == self._input:
                return name
        # Name not found, return index
        return self._input

    def input(self, description):
        """Change the input to the given description. The description must match
a key in the inputs dictionary field or be an integer matching
the receiver's input code."""
        if isinstance(description, (int, long)):
            self._sendCommand('%02dFN' % description)
        elif description in self.inputs:
            self._sendCommand('%02dFN' % self.inputs[description])
        else:
            raise Exception('No such input: %s' % description)

if __name__ == '__main__':
    receiver = Receiver()
    print 'Power', receiver.getPower()
    print 'Volume', receiver.getVolume()
