#!/usr/bin/env python

class Switch:
    off = 0
    on = 1
    toggle = 2

def ToggleSwitch(switch):
    if switch == Switch.off:
        return Switch.on
    else:
        return Switch.off

class ECError(Exception):
    """An error that occured in the entertainment center controls."""
    pass
