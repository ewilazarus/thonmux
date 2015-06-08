import logging
from shutil import which
from subprocess import Popen, PIPE

from . import exception

logger = logging.getLogger(__name__)


def _which_tmux():
    """Returns the path to the tmux executable"""

    logger.debug('Attempting to find tmux executable')
    ptmux = which('tmux')
    if not ptmux:
        logger.error("Didn't find tmux executable")
        raise exception.TmuxNotAvailable
    logger.debug('Found tmux executable in: "%s"' % ptmux)
    return ptmux


def _normalize(output):
    return [l.strip() for l in output.split('\n') if l != '']


def run(command):
    logger.info('Running command: tmux ' + ' '.join(command))
    ptmux = _which_tmux()
    args = [ptmux] + command

    with Popen(args, stdout=PIPE, stderr=PIPE, universal_newlines=True) as p:
        stdout, stderr = p.communicate()
        returncode = p.returncode
    stdout = _normalize(stdout)
    stderr = _normalize(stderr)
    logger.debug('return-code: ' + str(returncode))
    logger.debug('stdout: ' + str(stdout))
    logger.debug('stderr: ' + str(stderr))

    if returncode != 0:
        logger.debug('Command failed')
        exception.dispatcher(stderr[0])
    logger.debug('Command succeeded')
    return stdout
