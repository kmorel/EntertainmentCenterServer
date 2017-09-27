# A simple module that sends IR commands with LIRC. This is based off of
# code from https://github.com/loisaidasam/lirc-python, which itself is
# based off of code from https://github.com/slimjim777/web-irsend.

import subprocess
import time

class Lirc(object):
    """Provides simple commands to send command to LIRC through the irsend command.
Also does some parsing of the lircd.conf file to find available codes."""

    codes = {}

    def __init__(self, conf="/etc/lirc/lircd.conf"):
        self._parse(conf)

    def _parse(self, conf):
        """Parse the lircd.conf config file and create a dictionary.
        """
        remote_name = None
        code_section = False
        raw_code_section = False

        # Open the config file
        with open(conf, 'rb') as fp:
            for line in fp:
                # Convert tabs to spaces
                l = line.replace('\t',' ')

                # Look for a 'begin remote' line
                if l.strip()=='begin remote':
                    # Got the start of a remote definition
                    remote_name = None
                    code_section = False

                elif not remote_name and l.strip().find('name')>-1:
                    # Got the name of the remote
                    remote_name = l.strip().split(' ')[-1]
                    if remote_name not in self.codes:
                        self.codes[remote_name] = {}

                elif remote_name and l.strip()=='end remote':
                    # Got to the end of a remote definition
                    remote_name = None

                elif remote_name and l.strip()=='begin codes':
                    code_section = True

                elif remote_name and l.strip()=='end codes':
                    code_section = False

                elif remote_name and code_section:
                    # Got a code key/value pair... probably
                    fields = l.strip().split(' ')
                    self.codes[remote_name][fields[0]] = fields[-1]

                elif remote_name and l.strip()=='begin raw_codes':
                    raw_code_section = True

                elif remote_name and l.strip()=='end raw_codes':
                    raw_code_section = False

                elif remote_name and l.strip().find('name')>-1:
                    # Got name of command
                    code_name = l.strip().split(' ')[1]
                    if code_name not in self.codes[remote_name]:
                        self.codes[remote_name][code_name] = ''

    def devices(self):
        """Return a list of devices."""
        return self.codes.keys()


    def commands(self, device_id):
        """Return a list of commands for a device."""
        return self.codes[device_id].keys()

    def send(self, device_id, command, duration = 25):
        """Sends a particular device command. The duration parameter specifies how long
the command is sustained in milliseconds."""
        subprocess.call(['irsend', 'SEND_START', device_id, command])
        time.sleep(0.001*duration)
        subprocess.call(['irsend', 'SEND_STOP', device_id, command])
