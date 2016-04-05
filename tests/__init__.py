import time
import unittest

from thonmux import Thonmux


class ThonmuxTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Thonmux().kill_server()

    def setUp(self):
        # Give time for tmux to finish before starting it again
        time.sleep(0.05)
        self.t = Thonmux()

    def tearDown(self):
        Thonmux().kill_server()
