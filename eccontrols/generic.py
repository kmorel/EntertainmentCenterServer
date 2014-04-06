#!/usr/bin/env python

from lirc import lirc

from eccontrols import *

class GenericIR:
    """Sends IR signals to a particular device."""

    device = {}
    commands = {}

    def __init__(self, device):
        if not device in lirc.devices():
            raise ECError('No such device: %s' % device)
        self.device = device
        self.commands = lirc.commands(device)

    def send(self, command):
        """Send an IR code. Valid commands are listed in commands."""
        if command.upper() in self.commands:
            lirc.send(self.device, command.upper())
        else:
            raise ECError('No such command %s for device %s' % (command, self.device))

