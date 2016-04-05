import unittest

from . import binding_test

modules = [binding_test,]


suite = unittest.TestSuite()
for m in modules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(m))

unittest.TextTestRunner().run(suite)
