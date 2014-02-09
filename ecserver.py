
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
                                 start_mode_index=control.devices.index(control.getCurrentState()));

@web.route('/set-volume/<int:level>')
def set_volume(level):
    try:
        print 'Set volume: %s' % level
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
        control.changeMode(mode)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(mode)

@web.route('/tivo/ircommand/<ircode>')
def tivo_ircommand(ircode):
    try:
        print 'TiVo IR Code: %s' % ircode
        control.sendTiVo(ircode)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(ircode)

@web.route('/tivo/skip-back/<int:t>')
def tivo_skip_back(t):
    try:
        print 'TiVo Skip Back: %d' % t
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
        control.sendTiVoSecondsForward(t)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(t)

@web.route('/tivo/goto/<screen>')
def tivo_goto(screen):
    try:
        print 'TiVo Go To: %s' % screen
        control.gotoTiVoScreen(screen)
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e
    return str(screen)

@web.route('/log/<entry>')
def log(entry):
    try:
        print entry
    except Exception, e:
        print e.message
    except:
        e = sys.exc_info()[0]
        print e

if __name__ == '__main__':
    web.run(host='0.0.0.0', port=5000)
