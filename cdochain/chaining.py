#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Main module for chaining operation.

Idea is shamelessly stolen from:
    http://derrickgilland.com/posts/lazy-method-chaining-in-python/
    and
    https://github.com/dgilland/pydash/pydash/chaining.py
"""
from __future__ import absolute_import
from cdochain import exceptions
from cdo import Cdo


class Chain(object):
    """Main chain class for chaining of cdo operations."""

    def __init__(self, ifile, ofile, options="-O -f nc", lc=None):
        """Initialise environment of files.

        Arguments
        ---------
        ifile : str
            File on which to operate
        ofile : str
            Name of output file
        options : str
            Options used for writting to file
        lc : None or Wrapping
            Last command used

        Returns
        -------
        chain : Chain
            Chain object
        """
        self._ifile = ifile
        self._ofile = ofile
        self._opts = options
        self._last_command = lc

    def __getattr__(self, name):
        """Decide if given attribute is supported by cdo.

        Arguments
        ---------
        name : str
            Attribute being searched for

        Returns
        -------
        last_command : Wrapping
            The last command as a wrapping class object
        """
        if self.valid_cdo_method(name):
            if isinstance(self._last_command, Wrapping):
                self._ifile = self._last_command.to_cmdstr()
            self._last_command = Wrapping(self._ifile,
                                          name, self._ofile, self._opts)
        return self._last_command

    def __repr__(self):
        """String representation of objct."""
        return str(self.__dict__)

    @staticmethod
    def valid_cdo_method(name):
        """Valide cdo method.

        Arguments
        ---------
        name : str
            Method being searched for

        Returns:
        --------
        method : Object (function)
            executeable object function

        Raises:
        -------
        InvalidMethod Error if name can't be found.
        """
        method = getattr(Cdo(), name, False)
        if not callable(method):
            raise exceptions.InvalidMethod("Invalid method: {}".format(name))
        return method

    def execute(self):
        """Execute last command."""
        return self._last_command.execute() if self._last_command else False


class Wrapping(object):
    """Wrapping object for commands."""

    def __init__(self, ifile, method, of, op):
        """Wrapping object for commands in chain."""
        assert isinstance(ifile, str)
        assert isinstance(method, str)
        self.method = method
        self._ifile = ifile
        self.args = ()
        self.kwargs = {}
        self._of = of
        self._op = op

    def to_cmdstr(self):
        """Turn comamand in supported string format of cdo."""
        if self.args:
            return "-{},{} {}".format(self.method, self.args, self._ifile)
        return "-{} {}".format(self.method, self._ifile)

    def __call__(self, *args, **kwargs):
        """Save args and kwargs of method call as attributes."""
        self.args = ",".join([str(x) for x in list(args)])
        self.kwargs = kwargs
        s = self.__class__.__new__(self.__class__)
        s.__dict__ = self.__dict__.copy()
        return Chain(self._ifile, self._of, self._op, lc=s)

    def __repr__(self):
        """Return string representation of chain."""
        return self.to_cmdstr()

    def execute(self):
        """Execute chain."""
        f = getattr(Cdo(), self.method, None)
        if self.args:
            return f(self.args,
                     input=self._ifile,
                     output=self._of,
                     options=self._op)
        return f(input=self._ifile, output=self._of, options=self._op)


# def chain(value):
#     """Create 'Chain' object.
#
#     Creates a 'Chain' object which wraps the given value to enable
#     intuitive method chaining. Chaining is lazy and won't compute a value
#     until 'Chain.value' is called.
#     """
#     return Chain(value)
