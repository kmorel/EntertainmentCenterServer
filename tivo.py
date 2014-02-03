#!/usr/bin/env python

from common import Switch

import socket
import time

class TiVo:
    """Controls a TiVo DVR through a web interface."""
    hostname = '10.0.0.7'
    port = 31339

    _connection = None

    def _sendCommand(self, command):
        self._connection.send(command + '\r\n')

    def __init__(self):
        while not self._connection:
            try:
                self._connection = socket.create_connection((self.hostname,self.port))
            except socket.gaierror:
                print 'Bad connection. Trying again.'
        self._connection.setblocking(0)
        self._sendCommand('')
        time.sleep(0.1)

    screens = [ 'TiVo', 'LiveTV', 'Guide', 'NowPlaying' ]

    def teleport(self, screen):
        """Change the TiVo to the given screen. Valid screens are in the
screen field."""
        self._sendCommand('TELEPORT ' + screen)

    codes = [
        'UP',
        'DOWN',
        'LEFT',
        'RIGHT',
        'SELECT',
        'TIVO',
        'LIVETV',
        'GUIDE',
        'INFO',
        'EXIT',
        'THUMBSUP',
        'THUMBSDOWN',
        'CHANNELUP',
        'CHANNELDOWN',
        'PLAY',
        'FORWARD',
        'REVERSE',
        'PAUSE',
        'SLOW',
        'REPLAY',
        'ADVANCE',
        'RECORD'
    ]

    def ircode(self, code):
        """Send a code equivalent to a button on the IR remote. Some of the
codes are listed in the codes field."""
        self._sendCommand('IRCODE ' + code)

    def play(self):
        self.ircode('PLAY')

    def pause(self):
        self.ircode('PAUSE')

    def fastReverse(self):
        self.play()
        time.sleep(0.15)
        self.ircode('REVERSE')
        time.sleep(0.15)
        self.ircode('REVERSE')
        time.sleep(0.15)
        self.ircode('REVERSE')

    def fastForward(self):
        self.play()
        time.sleep(0.15)
        self.ircode('FORWARD')
        time.sleep(0.15)
        self.ircode('FORWARD')
        time.sleep(0.15)
        self.ircode('FORWARD')

    def back8sec(self):
        self.ircode('REPLAY')

    def back30sec(self):
        self.fastReverse()
        time.sleep(3.75)
        self.play()

    def back1min(self):
        self.fastReverse()
        time.sleep(7.5)
        self.play()

    def forward8sec(self):
        self.fastForward()
        time.sleep(1)
        self.play()

    def forward30sec(self):
        self.fastForward()
        time.sleep(3.75)
        self.play()

    def forward1min(self):
        self.fastForward()
        time.sleep(7.5)
        self.play()
