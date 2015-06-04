import logging
from shutil import which
from subprocess import Popen, PIPE

import exception

logger = logging.getLogger(__name__)


def _which_tmux():
    """Returns the path to the tmux executable"""

    logger.info('Attempting to find "tmux" executable')
    ptmux = which('tmux')
    if not ptmux:
        logger.error('Didn\'t find "tmux" executable')
        raise exception.TmuxNotAvailable
    logger.info('Found "tmux" executable in: "%s"' % ptmux)
    return ptmux

_ptmux = _which_tmux()


def _normalize(output):
    return [l for l in output.split('\n') if l != '']


class Binding:

    def run(self, command):
        """Returns the output of the executions of tmux with the given commands"""

        logger.info('Attempting to run command: tmux ' + ' '.join(command))
        args = [_ptmux] + command

        with Popen(args, stdout=PIPE, stderr=PIPE,
                   universal_newlines=True) as p:
            stdout, stderr = p.communicate()
            returncode = p.returncode
        self.returncode = returncode
        self.stdout = _normalize(stdout)
        self.stderr = _normalize(stderr)
        logger.debug('return-code: ' + str(returncode))
        logger.debug('stdout: ' + str(self.stdout))
        logger.debug('stderr: ' + str(self.stderr))

        if returncode != 0:
            logger.warning('Command failed')
            exception.dispatcher(self.stderr[0])
        logger.info('Command succeeded')
