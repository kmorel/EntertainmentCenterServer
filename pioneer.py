#!/usr/bin/env python

from common import Switch

import socket
import time

class Receiver:
    """Controls a Pioneer receiver through a web interface."""
    hostname = 'vsx-60.local'
    port = 23

    _connection = {}

    _power = Switch.off
    _volume = 0

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
        self._connection = socket.create_connection((self.hostname,self.port))
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

if __name__ == '__main__':
    receiver = Receiver()
    print 'Power', receiver.getPower()
    print 'Volume', receiver.getVolume()
