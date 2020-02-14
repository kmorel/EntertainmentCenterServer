#!/usr/bin/env python

from __future__ import print_function

from lirc import Lirc

from eccontrols import *

lirc = Lirc()

class GenericIR:
    """Sends IR signals to a particular device."""

    device = {}
    commands = {}
    duration = 25

    def __init__(self, device, duration=25):
        if not device in lirc.devices():
            raise ECError('No such device: %s' % device)
        self.device = device
        self.commands = lirc.commands(device)
        self.duration = duration

    def send(self, command):
        """Send an IR code. Valid commands are listed in commands."""
        if command.upper() in self.commands:
            lirc.send(self.device, command.upper(), self.duration)
        else:
            raise ECError('No such command %s for device %s' % (command, self.device))

    def __call__(self, command):
        self.send(command)

