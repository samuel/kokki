#!/usr/bin/env python

import os
import shutil
import tempfile
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

class TestExecute(unittest.TestCase):
    def setUp(self):
        self.temp_path = tempfile.mkdtemp(suffix="kokki-tests")

    def tearDown(self):
        shutil.rmtree(self.temp_path)

    def testOnlyIf(self):
        with Environment() as env:
            temp_file = os.path.join(self.temp_path, "exists")
            Execute("touch %s-lamba-false" % temp_file,
                only_if = lambda:False)
            Execute("touch %s-cmd-false" % temp_file,
                only_if = "false")
            Execute("touch %s-lambda-true" % temp_file,
                only_if = lambda:True)
            Execute("touch %s-cmd-true" % temp_file,
                only_if = "true")
            env.run()
        self.failIf(os.path.exists(temp_file+"-lambda-false"))
        self.failIf(os.path.exists(temp_file+"-cmd-false"))
        self.failUnless(os.path.exists(temp_file+"-lambda-true"))
        self.failUnless(os.path.exists(temp_file+"-cmd-true"))

if __name__ == '__main__':
    unittest.main()
