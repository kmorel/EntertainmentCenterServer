
import flask
web = flask.Flask(__name__)

@web.route('/')
def render_page():
    return flask.render_template('control-common.html')

@web.route('/set-volume/<volume>')
def set_volume(volume):
    print 'Set volume: %s' % volume
    return str(volume)

@web.route('/set-mute/<flag>')
def set_mute(flag):
    print 'Set mute: %s' % flag
    return str(flag)

if __name__ == '__main__':
    web.run()
