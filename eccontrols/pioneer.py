#!/usr/bin/env python

from __future__ import print_function

from eccontrols import *
from eccontrols.generic import GenericIR

import socket
import sys
import threading
import time

class ReceiverSocket:
    """Controls a Pioneer receiver through a web interface."""
    hostname = 'vsx-60.local'
    port = 23

    _connection = None
    _connectionLock = None

    _power = None
    _volume = None
    _mute = None
    _input = None

    # Would be better off in configuration
    inputs = {
        'Wii': 4,
        'DirecTV': 6,
        'Playstation 2': 15,
        'Fire TV': 19,
        'Chromecast': 22,
        'Switch-PS-XBox' : 21,
        'HDMI 6': 24,
        'Blu-Ray': 25
        }

    def _getStatus(self):
        print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Acquiring lock for receiver status")
        sys.stdout.flush()
        self._connectionLock.acquire()
        print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Lock acquired for receiver status")
        sys.stdout.flush()
        try:
            gotData = False
            while True:
                try:
                    data = self._connection.recv(1024).split()
                    gotData = True
                    for status in data:
                        print(status)
                        if status.startswith('PWR'):
                            if status[3] == '0':
                                self._power = Switch.on
                            elif status[3] == '1':
                                self._power = Switch.off
                            else:
                                print('Unknown power:', status[3:])
                        elif status.startswith('VOL'):
                            self._volume = int(status[3:])
                        elif status.startswith('MUT'):
                            if status[3] == '0':
                                self._mute = Switch.on
                            elif status[3] == '1':
                                self._mute = Switch.off
                            else:
                                print('Unknown mute:', status[3:])
                        elif status.startswith('FN'):
                            self._input = int(status[2:])
                except socket.error:
                    break;
        finally:
            self._connectionLock.release()
            print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Lock released for receiver status")
            sys.stdout.flush()
        return gotData

    def _flushStatus(self):
        print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Flushing Pioneer Receiver status.")
        sys.stdout.flush()
        self._getStatus()
        # Check again in 3 hours
        threading.Timer(108000, self._flushStatus).start()

    def _sendCommand(self, command, waitForResponse=False):
        print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Acquiring lock to send command", command, "to receiver")
        sys.stdout.flush()
        self._connectionLock.acquire()
        print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Lock acquired to send receiver command", command)
        sys.stdout.flush()
        try:
            self._getStatus()
            self._connection.send(command + '\r\n')
            if waitForResponse:
                # Wait for response by querying status, but only for 1 second
                startResponseTime = time.time()
                while (time.time() - startResponseTime) < 1.01:
                    if self._getStatus():
                        break
                    time.sleep(0.25)
        finally:
            self._connectionLock.release()
            print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Lock released to send receiver command", command)
            sys.stdout.flush()

    def __init__(self):
        self._connectionLock = threading.RLock()
        self._power = Switch.off
        self._volume = 100
        self._mute = Switch.off
        self._input = 6
        while not self._connection:
            try:
                self._connection = socket.create_connection((self.hostname,self.port))
            except socket.gaierror:
                print('Bad connection. Trying again.')
        self._connection.setblocking(0)
        self._sendCommand('')
        time.sleep(0.1)
        self._flushStatus()

    def getPower(self):
        self._sendCommand('?P', True)
        return self._power

    def power(self, flag=Switch.toggle):
        if flag == Switch.off:
            self._power = Switch.off
            self._sendCommand('PF')
        elif flag == Switch.on:
            self._power = Switch.on
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
        self._volume = value
        self._sendCommand('%03dVL' % value)

    def getMute(self):
        self._sendCommand('?M', True)
        return self._mute

    def mute(self, flag=Switch.toggle):
        if flag == Switch.off:
            self._mute = Switch.off
            self._sendCommand('MF')
        elif flag == Switch.on:
            self._mute = Switch.on
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
            self._input = description
            self._sendCommand('%02dFN' % description)
        elif description in self.inputs:
            self._input = self.inputs[description]
            self._sendCommand('%02dFN' % self.inputs[description])
        else:
            raise Exception('No such input: %s' % description)

class ReceiverIR(GenericIR):
    """Controls a Pioneer receiver through an IR interface."""

    # Would be better off in configuration
    inputs = {
        'Wii': 'INPUT-DVD',
        'DirecTV': 'INPUT-SAT-CBL',
        'Playstation 2': 'INPUT-DVD-BDR',
        'Fire TV': 'INPUT-HDMI-1',
        'Chromecast': 'INPUT-HDMI-4',
        'Switch-PS-XBox' : 'INPUT-HDMI-3',
        'HDMI 6': 'INPUT-HDMI-6',
        'Blu-Ray': 'INPUT-BD'
        }

    _power = None
    _volume = None
    _mute = None
    _input = None

    def __init__(self):
        GenericIR.__init__(self, 'PioneerReceiver')
        self._power = Switch.off
        self._volume = 111
        self._mute = Switch.off
        self._input = 'DirecTV'

    def getPower(self):
        return self._power

    def power(self, flag=Switch.toggle):
        if flag == Switch.toggle:
            flag = ToggleSwitch(self.getPower())
        if flag == Switch.off:
            self.send('power-off')
        elif flag == Switch.on:
            self.send('power-on')
        else:
            raise Exception('No such switch flag for power: %s' % flag)
        self._power = flag

    def getVolume(self):
        return self._volume

    def volume(self, value):
        """Set the volume. The volume is an integer in the range 0 to 185 where
0 is no volume, 1 is -80 dB, 161 is 0 dB, and 185 is +12 dB"""
        for i in xrange(self._volume, value):
            self.send('volume-up')
            time.sleep(0.05)
        for i in xrange(value, self._volume):
            self.send('volume-down')
            time.sleep(0.05)
        self._volume = value

    def getMute(self):
        return self._mute

    def mute(self, flag=Switch.toggle):
        if flag == Switch.toggle:
            flag = ToggleSwitch(self.getMute())
        if flag == Switch.off:
            self.send('mute-off')
        elif flag == Switch.on:
            self.send('mute-on')
        else:
            raise Exception('No such switch flag for power: %s' % flag)
        self._mute = flag

    def getInput(self):
        return self._input

    def input(self, description):
        """Change the input to the given description. The description must match
a key in the inputs dictionary field or be an integer matching
the receiver's input code."""
        if description in self.inputs:
            self.send(self.inputs[description])
            self._input = description
        else:
            raise Exception('No such input: %s' % description)

    # Configuration for socket interface
    socket_hostname = 'vsx-60.local'
    socket_port = 23

    # Would be better off in configuration
    socket_inputs = {
         4: 'Wii',
         6: 'DirecTV',
        15: 'Playstation 2',
        19: 'Fire TV',
        22: 'Chromecast',
        21: 'Switch-PS-XBox',
        24: 'HDMI 6',
        25: 'Blu-Ray'
        }

    def querySocket(self):
        """Attempts to connect to the receiver through its socket interface to
get its applicable state."""
        print("[", time.strftime("%Y-%m-%d %H:%M:%S"), "] Querying Pioneer Receiver status.")
        sys.stdout.flush()
        try:
            # Open connection
            connection = None
            for i in xrange(1, 6):
                print('Attempt', i)
                try:
                    connection = socket.create_connection((self.socket_hostname, \
                                                           self.socket_port))
                    break
                except socket.gaierror:
                    print('Connection attempt', i, 'failed.')

            if not connection:
                print('Failed to connect to receiver.')
                sys.stdout.flush()
                return

            connection.settimeout(2.0)

            # Send an empty string to 'wake up' receiver
            connection.send('\r\n')
            time.sleep(0.1)

            # Send query commands for power, mode, volume, and mute.
            connection.send('?F\r\n?P\r\n?V\r\n?M\r\n')

            # Read response from receiver until we get the mute response,
            # which is the last query command sent.
            gotmute = False
            while not gotmute:
                data = connection.recv(4096).split()
                for response in data:
                    print('  ', response)
                    if response.startswith('FN'):
                        input_num = int(response[2:])
                        self._input = self.socket_inputs[input_num]
                    elif response.startswith('PWR'):
                        if response[3] == '0':
                            self._power = Switch.on
                        elif response[3] == '1':
                            self._power = Switch.off
                        else:
                            print('Unknown power:', response[3:])
                    elif response.startswith('VOL'):
                        self._volume = int(response[3:])
                    elif response.startswith('MUT'):
                        gotmute = True
                        if response[3] == '0':
                            self._mute = Switch.on
                        elif response[3] == '1':
                            self._mute = Switch.off
                        else:
                            print('Unknown mute:', response[3:])

            connection.close()

        except socket.error as e:
            print("Socket error getting receiver state:", e.strerror)
        except:
            print("Unkown error getting receiver state:", sys.exc_info()[0])

        sys.stdout.flush()

if __name__ == '__main__':
    receiver = ReceiverIR()
    receiver.input('Blu-Ray')
    time.sleep(1)
    receiver.input('Fire TV')
    time.sleep(1)
    receiver.input('Chromecast')
    time.sleep(1)
    receiver.input('Wii')
    time.sleep(1)
    receiver.input('DirecTV')
    time.sleep(1)
    receiver.input('Playstation 2')
    time.sleep(1)
    receiver.input('HDMI 6')
    time.sleep(1)
    receiver.input('Switch-PS-XBox')

