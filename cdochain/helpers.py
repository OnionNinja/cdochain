#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Main module for chaining operation."""

from glob import glob as glb
import os
from cdo import Cdo
from cdochain.exceptions import InvalidOutput as ioe


def returntype_of_output(ofile):
    """Recognise if output parameter defines (masked) numpy array or file.

    Usage
    -----
    If file is input, then a None object will be returned.
    If 'array:<var>' is entered, a numpy array of <var> will be returned.
    If 'maarray:<var>' is entered, a masked numpy array of <var> will
    If 'netcdf4' is entered, a masked netcdf4.Dataset will
    be returned.
    """
    assert isinstance(ofile, str), "Output argument not a string value"
    if ofile[-3:] == '.nc':
        return None
    if ofile.lower() == 'netcdf4':
        return {'returnCdf': True}

    arr = ofile.split(':')
    try:
        if arr[0].lower() == 'array':
            return {'returnArray': arr[1]}
        if arr[0].lower() == "maarray":
            return {'returnMaArray': arr[1]}
    except IndexError:
        pass
    raise ioe('Return options not recognised, got {}'.format(ofile))


def formats(options):
    """Format options."""
    return ",".join([str(x) if not isinstance(x, str) else x for x in options])


def merge_input(ifile, ofile, options):
    """Function for putting out filenames correctly for CDO."""
    if isinstance(ifile, list) and len(ifile) > 1:
        tmpfile = os.path.basename(ofile)
        ifile = Cdo().mergetime(input=ifile, output='/tmp/'+tmpfile,
                                options=options)

    inputs = glb(ifile)

    if isinstance(ifile, str) and len(inputs) > 1:
        tmpfile = os.path.basename(ofile)
        ifile = Cdo().mergetime(input=inputs, output='/tmp/'+tmpfile,
                                options=options)
    return ifile
