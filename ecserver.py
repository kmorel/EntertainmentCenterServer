from __future__ import print_function

import flask
web = flask.Flask(__name__)

from control_central import *

import sys
import json

control = ControlCentral()

@web.route('/')
def render_page():
    try:
        return flask.render_template('control.html', \
                                     mute=int(control.getMute()), \
                                     mode_list=control.getModes(), \
                                     on_mode_list=control.getModes()[1:], \
                                     start_mode=control.getCurrentMode());
    except Exception as e:
        print(e.message)
        sys.stdout.flush()
    except:
        e = sys.exc_info()[0]
        print(e)
        sys.stdout.flush()

@web.route('/volume-down/<int:level>')
def volume_down(level):
    try:
        print('Volume down: %0.1f dB' % (0.5*level))
        sys.stdout.flush()
        control.volume_down(level)
    except Exception as e:
        print(e.message)
        return 'Volume down: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print(e)
        return 'Volume down error: %s' % e
    return 'Volume down: %0.1f' % (0.5*level)

@web.route('/volume-up/<int:level>')
def volume_up(level):
    try:
        print('Volume up: %0.1f dB' % (0.5*level))
        sys.stdout.flush()
        control.volume_up(level)
    except Exception as e:
        print(e.message)
        return 'Volume up: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print(e)
        return 'Volume up error: %s' % e
    return 'Volume up: %0.1f' % (0.5*level)

@web.route('/set-mute/<int:flag>')
def set_mute(flag):
    try:
        print('Set mute: %s' % flag)
        sys.stdout.flush()
        control.mute(flag)
    except Exception as e:
        print(e.message)
        return 'Set mute error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print(e)
        return 'Set mute error: %s' % e
    if control.getMute() == 0:
        return 'Set mute: off'
    else:
        return 'Set mute: on'

@web.route('/set-mode/<mode>')
def set_mode(mode):
    try:
        print('Set mode: %s' % mode)
        sys.stdout.flush()
        control.changeMode(mode)
    except Exception as e:
        print(e.message)
        return 'Set mode error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print(e)
        return 'Set mode error: %s' % e
    return 'Set mode: %s' % control.getCurrentState()

@web.route('/start/<mode>')
def set_mode_and_render_page(mode):
    try:
        print('Set mode: %s' % mode)
        sys.stdout.flush()
        control.changeMode(mode)
        return flask.render_template('control.html', \
                                     mute=int(control.getMute()), \
                                     volume=control.getVolume(), \
                                     mode_list=control.devices, \
                                     on_mode_list=control.devices[1:], \
                                     start_mode=control.getCurrentState());
    except Exception as e:
        print(e.message)
        sys.stdout.flush()
        return 'Set mode error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print(e)
        sys.stdout.flush()
        return 'Set mode error: %s' % e

@web.route('/receiver/cycle-power')
def cycle_receiver_power():
    try:
        print('Cycle receiver power')
        sys.stdout.flush()
        control.cycleReceiverPower()
        return 'Cycled receiver power'
    except Exception as e:
        print(e.message)
        sys.stdout.flush()
        return 'Cycle receiver power error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print(e)
        sys.stdout.flush()
        return 'Cycle receiver power error: %s' % e

@web.route('/send/<device>/<command>')
def send(device, command):
    try:
        print('Send %s, %s' % (device, command))
        sys.stdout.flush()
        control.send(device, command)
    except Exception as e:
        print(e.message)
        return 'Send %s error: %s' % (device, e.message)
    except:
        e = sys.exc_info()[0]
        print(e)
        return 'Send %s error: %s' % (device, e)
    return 'Sent: %s, %s' % (device, command)

@web.route('/status')
def status():
    state = {}
    state['mode'] = control.getCurrentState()
    state['mute'] = control.getMute()
    return json.dumps(state)

@web.route('/log/<entry>')
def log(entry):
    try:
        print(entry)
        sys.stdout.flush()
    except Exception as e:
        print(e.message)
    except:
        e = sys.exc_info()[0]
        print(e)

if __name__ == '__main__':
    web.run(host='0.0.0.0', port=80)
