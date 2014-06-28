
import flask
web = flask.Flask(__name__)

from control_central import *

import sys

control = ControlCentral()

@web.route('/')
def render_page():
    return flask.render_template('control.html', \
                                 mute=int(control.getMute()), \
                                 volume=control.getVolume(), \
                                 mode_list=control.devices, \
                                 on_mode_list=control.devices[1:], \
                                 start_mode=control.getCurrentState());

@web.route('/set-volume/<int:level>')
def set_volume(level):
    try:
        print 'Set volume: %s' % level
        sys.stdout.flush()
        control.volume(level)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(level)

@web.route('/set-mute/<int:flag>')
def set_mute(flag):
    try:
        print 'Set mute: %s' % flag
        sys.stdout.flush()
        control.mute(flag)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(flag)

@web.route('/set-mode/<mode>')
def set_mode(mode):
    try:
        print 'Set mode: %s' % mode
        sys.stdout.flush()
        control.changeMode(mode)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(mode)

@web.route('/receiver/send/<command>')
def receiver_send(command):
    try:
        print 'Receiver IR Code: %s' % command
        sys.stdout.flush()
        control.sendReceiver(command)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(command)

@web.route('/tivo/send/<command>')
def tivo_send(command):
    try:
        print 'TiVo IR Code: %s' % command
        sys.stdout.flush()
        control.sendTiVo(command)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(command)

@web.route('/tivo/skip-back/<int:t>')
def tivo_skip_back(t):
    try:
        print 'TiVo Skip Back: %d' % t
        sys.stdout.flush()
        control.sendTiVoSecondsBack(t)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(t)

@web.route('/tivo/skip-forward/<int:t>')
def tivo_skip_forward(t):
    try:
        print 'TiVo Skip Forward: %d' % t
        sys.stdout.flush()
        control.sendTiVoSecondsForward(t)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(t)

# @web.route('/tivo/goto/<screen>')
# def tivo_goto(screen):
#     try:
#         print 'TiVo Go To: %s' % screen
#         sys.stdout.flush()
#         control.gotoTiVoScreen(screen)
#     except Exception, e:
#         print e.message
#     except:
#         e = sys.exc_info()[0]
#         print e
#     return str(screen)

@web.route('/tv/send/<command>')
def tv_send(command):
    try:
        print 'TV Command:', command
        sys.stdout.flush()
        control.sendTV(command)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(command)

@web.route('/bluray/send/<command>')
def bluray_send(command):
    try:
        print 'Blu-Ray Command:', command
        sys.stdout.flush()
        control.sendBluRay(command)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(command)

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
