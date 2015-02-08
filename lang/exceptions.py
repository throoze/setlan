#!/usr/bin/env python
# ------------------------------------------------------------
# exceptions.py
#
# Exceptions for the language Setlan
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------

class SetlanException(Exception):

    def __init__(self, error, *args, **kwargs):
        super(SetlanException, self).__init__(args,kwargs)
        self._error = error

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()


class SetlanInputNotDefinedException(SetlanException):

    def __unicode__(self):
        string = "SetlanInputNotDefinedException: %s" % self._error
        return string


class SetlanTokensNotDefinedException(SetlanException):

    def __unicode__(self):
        string = "SetlanTokensNotDefinedException: %s" % self._error
        return string


class SetlanLexicalErrors(SetlanException):

    def __init__(self, errors, *args, **kwargs):
        error = "Lexical errors were found:"
        super(SetlanLexicalErrors, self).__init__(error, args, kwargs)
        self._errors = errors

    def __unicode__(self):
        string = "SetlanLexicalErrors: %s" % self._error
        for error in self._errors:
            string += "\n\t%s" % error
        return string


class SetlanLexicalError(SetlanException):

    def __unicode__(self):
        string = "SetlanLexicalError: %s" % self._error
        return string


class SetlanValueError(SetlanException):

    def __unicode__(self):
        string = "SetlanValueError: %s" % self._error
        return string


class SetlanSyntaxError(SetlanException):

    def __unicode__(self):
        string = "SetlanSyntaxError: %s" % self._error
        return string