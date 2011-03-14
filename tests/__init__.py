#!/usr/bin/env python

import os
import unittest
from kokki import *

class TestKitchen(unittest.TestCase):
    def setUp(self):
        self.kit = Kitchen()
        self.kit.add_cookbook_path("kokki.cookbooks", os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookbooks"))

    def testUnknownConfig(self):
        self.failUnlessRaises(AttributeError, lambda:self.kit.config.test.config1)

    def testDefaultConfig(self):
        self.kit.include_recipe("test")
        self.kit.run()

        self.failUnlessEqual("fu", self.kit.config.test.config1)
        self.failUnlessEqual("manchu", self.kit.config.test.config2)
        self.failUnlessEqual("manchu", self.kit._test)

    def testOverrideConfig(self):
        self.kit.update_config({"test.config1": "bar"})
        self.kit.include_recipe("test")
        self.kit.run()

        self.failUnlessEqual("bar", self.kit.config.test.config1)
        self.failUnlessEqual("manchu", self.kit.config.test.config2)
        self.failUnlessEqual("manchu", self.kit._test)

if __name__ == '__main__':
    unittest.main()
