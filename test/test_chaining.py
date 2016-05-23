#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Tests for chaining module."""

import pytest
from cdochain import chaining as ch
from cdochain import exceptions as ex


def test_initializing():
    """Test if initilalisation is working."""
    init = ch.Chain("init")
    assert isinstance(init, ch.Chain)


def test_invalid_method():
    """Test if invalid input raises proper exception."""
    init = ch.Chain("init")
    with pytest.raises(ex.InvalidMethod):
        init.coolmean("32")


def test_valid_method():
    """Test if one valid input is accepted."""
    init = ch.Chain("init")
    init.mermean("32")
