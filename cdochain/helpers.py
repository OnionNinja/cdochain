#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Main module for chaining operation."""


def formats(options):
    return ",".join([str(x) if not isinstance(x, str) else x for x in options])
