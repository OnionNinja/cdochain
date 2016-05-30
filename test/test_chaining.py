#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Tests for chaining module."""

# import pytest
# from cdochain import chaining as ch
# from cdochain import exceptions as ex
from cdochain import helpers as hlp
import cdochain.chaining as cch
import cdo
import netCDF4 as ncd
import numpy as np
import os


class Test_Calculations(object):
    """Test of proper calculations and workings."""

    def setup(self):
        """Setup process."""
        self.ifile = './test/testdata/sresa1b_ncar_ccsm3-example.nc'
        cdomethods = cdo.Cdo()
        self.tmp_iter = cdomethods.mermean(input=self.ifile,
                                           output=self.ifile[:-3]+'-mer.nc',
                                           options="-O -f nc")
        self.final = cdomethods.zonmean(input=self.tmp_iter,
                                        output=self.ifile[:-3]+'-mer-zon.nc',
                                        options="-O -f nc")
        self.data_iter = ncd.Dataset(self.final)

        tmp_at_one_go = "-mermean "+self.ifile
        self.final_str = cdomethods.zonmean(input=tmp_at_one_go,
                                            output=self.ifile[:-3] +
                                            '-mer-zon-str.nc',
                                            options="-O -f nc")
        self.datas = ncd.Dataset(self.final_str)

    def teardown(self):
        """Teardown process."""
        os.remove(self.tmp_iter)
        os.remove(self.final)
        os.remove(self.final_str)

    def test_setup(self):
        """Test if setup was successfull."""
        assert np.array_equal(self.data_iter['tas'][:], self.datas['tas'][:])

    def test_single_concatination(self):
        """Test if cdochain works with only one input."""
        routine = cch.Chain(self.ifile,
                            self.tmp_iter[:-3]+'-mer-ch.nc',
                            '-O -f nc')
        meridian = routine.mermean()
        res = meridian.result()
        assert np.array_equal(ncd.Dataset(res['tas'][:]),
                              self.data_iter['tas'][:])


def test_format_inputs():
    """Test if formating of options works."""
    assert hlp.formats(['235', 532, 412]) == '235,532,412'
    assert hlp.formats(('235', 532, 412)) == '235,532,412'
    assert hlp.formats(['ifile', 532, '412']) == 'ifile,532,412'
    assert isinstance(hlp.formats(['ifile', 532, '412']), str)

# def test_initializing():
#     """Test if initilalisation is working."""
#     init = ch.Chain("inputfile", "outputfile", "options")
#     assert isinstance(init, ch.Chain)

# def test_invalid_method():
#     """Test if invalid input raises proper exception."""
#     init = ch.Chain("inputfile", "outputfile", "options")
#     with pytest.raises(ex.InvalidMethod):
#         init.coolmean("32")

# def test_valid_method():
#     """Test if one valid input is accepted."""
#     init = ch.Chain("inputfile", "outputfile", "options")
#     init.mermean("32")
