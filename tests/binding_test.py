from thonmux.binding import run
from thonmux.exception import IllegalCommand

from . import ThonmuxTestCase


class BindingTestCase(ThonmuxTestCase):

    def test_can_run_legal_command(self):
        self.t.new_session('thonmux-test-session')
        result = run(['list-sessions'])
        self.assertEqual(len(result), 1)

    def test_cant_run_illegal_command(self):
        with self.assertRaises(IllegalCommand):
            run(['this', 'is', 'an', 'illegal', 'command'])
