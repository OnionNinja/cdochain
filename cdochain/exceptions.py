#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""Exceptions in cdochain."""


class ChainException(Exception):
    """Base class for exceptions thrown by cdochain."""

    def __init__(self, message):
        """Initialization of exceptions."""
        super(ChainException, self).__init__(self, message)
        self.message = message

    def __str__(self):
        """String representation."""
        return repr(self.message)

    def format_message(self):
        """Error message format."""
        return self.message


class InvalidMethod(ChainException):
    """Error message if chaining gets an invalid method."""
    pass


class InvalidOutput(ChainException):
    """Error message for unrecognized Output parameters."""
    pass
