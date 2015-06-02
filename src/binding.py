import logging
from shutil import which
from subprocess import check_output, CalledProcessError, DEVNULL

from util import PymuxException

_logger = logging.getLogger(__name__)


def _which_tmux():
    """Returns the path to the tmux executable"""

    print('oi')
    _logger.info('Attempting to find "tmux" executable')
    ptmux = which('tmux')
    if not ptmux:
        _logger.error('Didn\'t find "tmux" executable')
        raise PymuxException('''The executable "tmux" was not found. Make sure
                             it is installed and available in the $PATH.''')
    _logger.info('Found "tmux" executable in: "%s"' % ptmux)
    return ptmux

_ptmux = _which_tmux()


def _normalize(output):
    """Returns a list with the normalized output's lines"""

    return [line for line in output.split('\n') if line != '']


def run(command):
    """Returns the output of the executions of tmux with the given commands"""

    _logger.info('Attempting to run command: tmux ' + command)
    args = [_ptmux] + command.split()
    try:
        output = check_output(args, stderr=DEVNULL).decode()
        return _normalize(output)
    except (OSError, CalledProcessError):
        _logger.error('Failed to run the command: tmux ' + command)
        raise PymuxException('''The command "tmux {}" is not a valid tmux
                                 command.'''.format(command))
