#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Main module for chaining operation."""

from glob import glob as glb
import os
from cdo import Cdo


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
