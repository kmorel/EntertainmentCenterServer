
import flask
web = flask.Flask(__name__)

from control_central import *

import sys

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
        return 'Set mode error: %s' % e
    except:
        e = sys.exc_info()[0]
        print e
        return 'Set mode error: %s' % e
    return 'Set mode: %s' % control.getCurrentState()

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

@web.route('/tivo/send/<command>')
def tivo_send(command):
    try:
        print 'TiVo IR Code: %s' % command
        sys.stdout.flush()
        control.sendTiVo(command)
    except Exception, e:
        print e.message
        return 'Send TiVo error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Send TiVo error: %s' % e
    return 'Sent: TiVo, %s' % command

@web.route('/tivo/skip-back/<int:t>')
def tivo_skip_back(t):
    try:
        print 'TiVo Skip Back: %d' % t
        sys.stdout.flush()
        control.sendTiVoSecondsBack(t)
    except Exception, e:
        print e.message
        return 'Send TiVo back error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Send TiVo back error: %s' % e
    return 'Sent: Tivo, back-%d-seconds' % t

@web.route('/tivo/skip-forward/<int:t>')
def tivo_skip_forward(t):
    try:
        print 'TiVo Skip Forward: %d' % t
        sys.stdout.flush()
        control.sendTiVoSecondsForward(t)
    except Exception, e:
        print e.message
        return 'Send TiVo forward error: %s' % e.message
    except:
        e = sys.exc_info()[0]
        print e
        return 'Send TiVo forward error: %s' % e
    return 'Sent: Tivo, forward-%d-seconds' % t

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
