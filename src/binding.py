import logging
from shutil import which
from subprocess import Popen, PIPE

from util import ThonmuxException

logger = logging.getLogger(__name__)


def _which_tmux():
    """Returns the path to the tmux executable"""

    logger.info('Attempting to find "tmux" executable')
    ptmux = which('tmux')
    if not ptmux:
        logger.error('Didn\'t find "tmux" executable')
        message = 'The executable "tmux" was not found. Make sure it is \
                installed and available in the $PATH.'
        raise ThonmuxException(message)
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
            out, err = p.communicate()
        self.stdout = _normalize(out)
        self.stderr = _normalize(err)

        if len(self.stderr) > 0:
            logger.warning('Failed to run the command: tmux ' +
                         ' '.join(command))
            message = 'The command "tmux %s" is not a valid tmux command.' % (
                      ' '.join(command))
            raise ThonmuxException(message)
