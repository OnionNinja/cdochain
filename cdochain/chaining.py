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
from cdochain import helpers as hlp


class Chain(object):
    """Main chain class for chaining of cdo operations."""

    def __init__(self, ifile, ofile, options="-O -f nc"):
        """Initialise environment of files.

        Arguments
        ---------
        ifile : str
            File on which to operate
        ofile : str
            Name of output file
        options : str
            Options used for writting to file

        Attributes
        -----------
        lc : None or Wrapping
            Last command used

        Returns
        -------
        chain : Chain
            Chain object
        """
        # first merge files if several files are declared as input
        self._ifile = hlp.merge_input(ifile, ofile, options)
        self._ofile = ofile
        self._opts = options
        self._last_command = None

    def _generate(self):
        """Generate a copy of this instance."""
        new = self.__class__.__new__(self.__class__)
        new.__dict__ = self.__dict__.copy()
        return new

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
        wrapper = self._generate()

        if wrapper.valid_cdo_method(name):
            if isinstance(wrapper._last_command, Wrapping):
                wrapper._ifile = wrapper._last_command.to_cmdstr()
            wrapper._last_command = Wrapping(wrapper._ifile,
                                             name, wrapper._ofile,
                                             wrapper._opts)
        return wrapper._last_command

    def __repr__(self):
        """String representation of objct."""
        val = {'ifile': self._ifile,
               'ofile': self._ofile,
               'options': self._opts}
        if self._last_command:
            val['last_command'] = str(self._last_command)
        else:
            val['last_command'] = None

        return str(val)

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
        """Turn command in supported string format of cdo."""
        if self.args:
            return "-{},{} {}".format(self.method, self.args, self._ifile)
        return "-{} {}".format(self.method, self._ifile)

    def _generate(self):
        """Generate a copy of this instance."""
        new = self.__class__.__new__(self.__class__)
        new.__dict__ = self.__dict__.copy()
        return new

    def __call__(self, *args, **kwargs):
        """Save args and kwargs of method call as attributes."""
        self.args = hlp.formats(args)
        self.kwargs = kwargs

        wrapper = self._generate()
        new_chain = Chain(self._ifile, self._of, self._op)
        new_chain._last_command = wrapper

        return new_chain

    def __repr__(self):
        """Return string representation of chain."""
        return self.to_cmdstr()

    def execute(self):
        """Execute chain."""
        self._special_return = hlp.check_if_special_return(self._of)
        f = getattr(Cdo(), self.method, None)
        if self._special_return and self.args:
            return f(self.args, input=self._ifile, options=self._op,
                     **self._special_return)
        elif self.args:
            return f(self.args, input=self._ifile, output=self._of,
                     options=self._op)
        if self._special_return:
            return f(input=self._ifile, options=self._op,
                     **self._special_return)
        return f(input=self._ifile, output=self._of, options=self._op)


# def chain(value):
#     """Create 'Chain' object.
#
#     Creates a 'Chain' object which wraps the given value to enable
#     intuitive method chaining. Chaining is lazy and won't compute a value
#     until 'Chain.value' is called.
#     """
#     return Chain(value)
