from nose.tools import raises

import binding
import util


def run_test_dumb():
    binding.run('list-sessions')


@raises(util.PymuxException)
def run_test_failure():
    binding.run('doesnotexist')
