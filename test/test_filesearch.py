#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Tests for filesearch module."""

import os
import glob


class Test_Filesearch(object):
    """Tests for file search ability.

    Tests for filesearch ability in case of merge-operations
    of cdo toolset.
    """

    def setup(self):
        self.ifile = './test/testdata/sresa1b_ncar_ccsm3-example.nc'
        self.ofile = self.ifile[:-3]+'tmp.nc'
        self.outsi = './test/outside-example.nc'
        self.text = './test/testdata/test.txt'
        open(self.ofile, 'a').close()
        open(self.outsi, 'a').close()

    def teardown(self):
        os.remove(self.ifile)
        os.remove(self.ofile)
        os.remove(self.outsi)
        os.remove(self.text)

    def test_glob(self):
        assert len(glob.glob('.')) == 1
        assert len(glob.glob('./testdata/')) == 3
        assert len(glob.glob('./testdata/*.txt')) == 1
        assert len(glob.glob('./testdata/*.nc')) == 2
        assert len(glob.glob('./testdata/test*')) == 1
        assert len(glob.glob('./testdata/test*t')) == 1
