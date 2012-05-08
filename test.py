#!/usr/bin/env python
import unittest
from . import util, svn

class TestSVN(unittest.TestCase):
    def setUp(self):
        self.svn = svn.svn('/home/dong/projects/sae/apps/ddliu')

    def test_info(self):
        info = self.svn.info()
        self.assertRegexpMatches(info['revision'], '^\d+$', 'revision is numeric')

    def test_update(self):
        pass

    def test_commit(self):
        pass

class TestSync(unittest.TestCase):
    def setUp(self):
        pass

    def test_sync(self):
        print('aa')
        pass

if __name__ == '__main__':
    unittest.main()