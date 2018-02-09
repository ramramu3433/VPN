from os import chdir
from subprocess import Popen, PIPE
import logging

FORMAT = '%(asctime) - %(VPN) - %(User) -%(password) - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger('VPN')

chdir('C:\\Program Files (x86)\\CheckPoint\\Endpoint Connect')


class VPN:
    def __init__(self, server, user, password):

        self.site = server
        self.user = user
        self.password = password
        self.d = {'VPN': server, 'User': user, 'password': password}

    @property
    def connect(self):
        command = ['trac.exe', 'connect', '-s', self.site, '-u', self.user, '-p', self.password]

        t = Popen(command, stdout=PIPE, stderr=PIPE)
        output, errors = t.communicate()
        # print output, errors

        if "Connection was successfully established" in output:
            logger.info(output, extra=self.d)
            return 0
        elif "Client is already connected to another site. Please disconnect first." in output:
            self.disconnect()
            self.connect
        elif "Connection could not be established - Client is already connected" in output:
            logger.error(output, extra=self.d)
            return 0
        elif "Access denied - wrong user name or password" in output:
            logger.error(output, extra=self.d)
            return 1
        elif "Connection could not be established: Negotiation with site failed" in output:
            logger.error(output, extra=self.d)
            return 2
            self.connect
        elif "Connection could not be established - A previous connection is currently on progress" in output:
            logger.error(output, extra=self.d)
            self.disconnect()
            self.connect

    def disconnect(self):
        command2 = ['trac.exe', 'disconnect']
        t = Popen(command2, stdout=PIPE, stderr=PIPE)
        output, errors = t.communicate()
        if "Connection was successfully disconnected" in output:
            logger.info(output, extra=self.d)
            return 1
        else:
            logger.error(output, extra=self.d)
            return 0
