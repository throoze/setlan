#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# config.py
#
# Global Setlan minor configuration parameters.
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------

class SetlanConfig(object):
    """Global configuration for Setlan language structures"""

    VERSION = '0.3'

    SUCCESS = 0
    ERR_BAD_USAGE = 1
    ERR_BAD_FILENAME = 2
    ERR_IO_ERROR = 3
    ERR_LEXICOGRAPHICAL_ERROR = 4
    ERR_VALUE_ERROR = 5
    ERR_INPUT_NOT_PROVIDED = 6
    ERR_LANG_LEX_MODULE_NOT_PROVIDED = 7
    ERR_SYNTAX_ERROR = 8
    ERR_STATIC_ERROR = 9
    ERR_SCOPE_ERROR = 10
    ERR_TYPE_ERROR = 11
    #ERR_ZERO_DIVISION = 12

    SPACE = "    "

    def __init__(self, *args, **kwargs):
        super(SetlanConfig, self).__init__()

    def _get_indentation(self, level):
        return level * self.SPACE
