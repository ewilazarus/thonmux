from nose.tools import raises

import binding
import util


def run_test_dumb():
    b = binding.Binding()
    b.run(['list-sessions'])


@raises(util.ThonmuxException)
def run_test_failure():
    b = binding.Binding()
    b.run(['doesnotexist'])
