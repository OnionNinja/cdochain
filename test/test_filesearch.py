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
        open(self.ofile, 'a').close()
        open(self.outsi, 'a').close()

    def teardown(self):
        os.remove(self.ifile)
        os.remove(self.ofile)
        os.remove(self.outsi)

    def test_recursive(self):
        assert len(glob.glob('.')) == 1
