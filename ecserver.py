
import flask
web = flask.Flask(__name__)

@web.route('/')
def render_page():
    return flask.render_template('control.html', \
                                 mute=int(False), \
                                 volume=101, \
                                 mode_list=['TiVo', 'Blu-Ray', 'XBox 360', 'Wii', 'Playstation 2', 'Turn Everything Off']);

@web.route('/set-volume/<volume>')
def set_volume(volume):
    print 'Set volume: %s' % volume
    return str(volume)

@web.route('/set-mute/<int:flag>')
def set_mute(flag):
    print 'Set mute: %s' % flag
    return str(flag)

@web.route('/set-mode/<mode>')
def set_mode(mode):
    print 'Set mode: %s' % mode
    return str(mode)

@web.route('/log/<entry>')
def log(entry):
    print entry

if __name__ == '__main__':
    web.run()
