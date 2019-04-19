
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
                                     volume=control.getVolume(), \
                                     mode_list=control.devices, \
                                     on_mode_list=control.devices[1:], \
                                     start_mode=control.getCurrentState());
    except Exception, e:
        print e.message
        sys.stdout.flush()
    except:
        e = sys.exc_info()[0]
        print e
        sys.stdout.flush()


@web.route('/set-volume/<int:level>')
def set_volume(level):
    try:
        print 'Set volume: %d' % level
        sys.stdout.flush()
        control.volume(level)
    except Exception, e:
        print e.message
        return 'Set volume error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Set volume error: %s' % e
    return 'Set volume: %d' % control.getVolume()

@web.route('/set-mute/<int:flag>')
def set_mute(flag):
    try:
        print 'Set mute: %s' % flag
        sys.stdout.flush()
        control.mute(flag)
    except Exception, e:
        print e.message
        return 'Set mute error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Set mute error: %s' % e
    if control.getMute() == 0:
        return 'Set mute: off'
    else:
        return 'Set mute: on'

@web.route('/set-mode/<mode>')
def set_mode(mode):
    try:
        print 'Set mode: %s' % mode
        sys.stdout.flush()
        control.changeMode(mode)
    except Exception, e:
        print e.message
        return 'Set mode error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Set mode error: %s' % e
    return 'Set mode: %s' % control.getCurrentState()

@web.route('/start/<mode>')
def set_mode_and_render_page(mode):
    try:
        print 'Set mode: %s' % mode
        sys.stdout.flush()
        control.changeMode(mode)
        return flask.render_template('control.html', \
                                     mute=int(control.getMute()), \
                                     volume=control.getVolume(), \
                                     mode_list=control.devices, \
                                     on_mode_list=control.devices[1:], \
                                     start_mode=control.getCurrentState());
    except Exception, e:
        print e.message
        sys.stdout.flush()
        return 'Set mode error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        sys.stdout.flush()
        return 'Set mode error: %s' % e

@web.route('/receiver/cycle-power')
def cycle_receiver_power():
    try:
        print 'Cycle receiver power'
        sys.stdout.flush()
        control.cycleReceiverPower()
        return 'Cycled receiver power'
    except Exception, e:
        print e.message
        sys.stdout.flush()
        return 'Cycle receiver power error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        sys.stdout.flush()
        return 'Cycle receiver power error: %s' % e

@web.route('/receiver/send/<command>')
def receiver_send(command):
    try:
        print 'Receiver IR Code: %s' % command
        sys.stdout.flush()
        control.sendReceiver(command)
    except Exception, e:
        print e.message
        return 'Send receiver error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Send receiver error: %s' % e
    return 'Sent: Receiver, %s' % command

@web.route('/directv/send/<command>')
def directv_send(command):
    try:
        print 'DirecTV IR Code: %s' % command
        sys.stdout.flush()
        control.sendDirecTV(command)
    except Exception, e:
        print e.message
        return 'Send DirecTV error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Send DirecTV error: %s' % e
    return 'Sent: DirecTV, %s' % command

@web.route('/tv/send/<command>')
def tv_send(command):
    try:
        print 'TV Command:', command
        sys.stdout.flush()
        control.sendTV(command)
    except Exception, e:
        print e.message
        return 'Send TV error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Send TV error: %s' % e
    return 'Sent: TV, %s' % command

@web.route('/bluray/send/<command>')
def bluray_send(command):
    try:
        print 'Blu-Ray Command:', command
        sys.stdout.flush()
        control.sendBluRay(command)
    except Exception, e:
        print e.message
        return 'Send Blu-Ray error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Send Blu-Ray error: %s' % e
    return 'Sent: Blu-Ray, %s' % command

@web.route('/status')
def status():
    state = {}
    state['mode'] = control.getCurrentState()
    state['volume'] = control.getVolume()
    state['mute'] = control.getMute()
    return json.dumps(state)

@web.route('/log/<entry>')
def log(entry):
    try:
        print entry
        sys.stdout.flush()
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e

if __name__ == '__main__':
    web.run(host='0.0.0.0', port=80)
