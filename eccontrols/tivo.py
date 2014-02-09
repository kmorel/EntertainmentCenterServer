#!/usr/bin/env python

from eccontrols import *

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
        if screen in self.screens:
            self._sendCommand('TELEPORT ' + screen)
        else:
            print 'No such screen: %s' % screen

    codes = {
        'up': 'UP',
        'down': 'DOWN',
        'left': 'LEFT',
        'right': 'RIGHT',
        'select': 'SELECT',
        'tivo': 'TIVO',
        'live-tv': 'LIVETV',
        'guide': 'GUIDE',
        'info': 'INFO',
        'return': 'EXIT',
        'thumbs-up': 'THUMBSUP',
        'thumbs-down': 'THUMBSDOWN',
        'channel-up': 'CHANNELUP',
        'channel-down': 'CHANNELDOWN',
        'play': 'PLAY',
        'seek-forward': 'FORWARD',
        'seek-back': 'REVERSE',
        'pause': 'PAUSE',
        'slow': 'SLOW',
        'back-8-sec': 'REPLAY',
        'skip': 'ADVANCE',
        'record': 'RECORD'
    }

    def ircode(self, code):
        """Send a code equivalent to a button on the IR remote. The codes are
defined in the codes field."""
        if code.lower() in self.codes:
            self._sendCommand('IRCODE ' + self.codes[code.lower()])
        else:
            print 'No such code: %s' % code

    def fastReverse(self):
        self.ircode('play')
        time.sleep(0.2)
        self.ircode('seek-back')
        time.sleep(0.2)
        self.ircode('seek-back')
        time.sleep(0.2)
        self.ircode('seek-back')

    def fastForward(self):
        self.ircode('play')
        time.sleep(0.2)
        self.ircode('seek-forward')
        time.sleep(0.2)
        self.ircode('seek-forward')
        time.sleep(0.2)
        self.ircode('seek-forward')

    def secondsBack(self, t):
        if int(t) < 9:
            self.ircode('back-8-sec')
        else:
            self.fastReverse()
            time.sleep(float(t)/32)
            self.ircode('seek-back')
            time.sleep(0.05)
            self.ircode('play')

    def secondsForward(self, t):
        self.fastForward()
        time.sleep(float(t)/32)
        self.ircode('seek-forward')
        time.sleep(0.05)
        self.ircode('play')

