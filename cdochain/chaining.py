#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Main module for chaining operation.

Shamelessly stolen from:
    http://derrickgilland.com/posts/lazy-method-chaining-in-python/
    and
    https://github.com/dgilland/pydash/pydash/chaining.py
"""
from __future__ import absolute_import
from cdochain.exceptions import InvalidMethod
import cdo


class Chain(object):
    """Enables chaining of cdo functions."""

    def __init__(self, ifiles, ofiles, opts):
        """Initialize 'Chain' object."""
        self._ifiles = ifiles
        self._ofiles = ofiles
        self._opts = opts

    def value(self):
        """Return current value of the chain operations."""
        if isinstance(self._value, ChainWrapper):
            self._value = self._value.unwrap()
        return self._value

    @staticmethod
    def get_method(name):
        """Return valid cdo method."""
        cdoobj = cdo.Cdo()
        method = getattr(cdoobj, name, None)

        if not callable(method):
            raise InvalidMethod('Invalid cdo method: {0}'.format(name))

        return method

    def __getattr__(self, attr):
        """Proxy attribute access to cdo."""
        return ChainWrapper(self._value, self.get_method(attr))


class ChainWrapper(object):
    """Wrap cdo method call within a ChainWrapper context."""

    def __init__(self, value, method):
        """Initialize wrapper."""
        self._value = value
        self.method = method
        self.args = ()
        self.kargs = {}

    def unwrap(self):
        """Execute method with _value, args, and kargs.

        If _value is an instance of ChainWrapper,
        then unwrap it before calling method.
        """
        if isinstance(self._value, ChainWrapper):
            self._value = self._value.unwrap()
        return self.method(self._value, *self.args, **self.kargs)

    def __call__(self, *args, **kargs):
        """Invoke the method.

        Invoke the method with value as the first argument and return a new
        Chain object with the return value.
        """
        self.args = args
        self.kargs = kargs
        return Chain(self)


def chain(value):
    """Create 'Chain' object.

    Creates a 'Chain' object which wraps the given value to enable
    intuitive method chaining. Chaining is lazy and won't compute a final value
    until 'Chain.value' is called.
    """
    return Chain(value)
