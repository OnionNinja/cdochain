#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Main module for chaining operation."""


def formats(options):
    """Format options."""
    return ",".join([str(x) if not isinstance(x, str) else x for x in options])


def filesearch(filename):
    """Function for putting out filenames correctly for CDO."""
    pass
