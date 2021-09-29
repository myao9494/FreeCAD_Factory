# -*- coding: utf-8 -*-
#***********************************************************************
#* Copyright (c) 2019 Joel Graff <monograff76@gmail.com>               *
#*                                                                     *
#* This program is free software; you can redistribute it and/or modify*
#* it under the terms of the GNU Lesser General Public License (LGPL)  *
#* as published by the Free Software Foundation; either version 2 of   *
#* the License, or (at your option) any later version.                 *
#* for detail see the LICENCE text file.                               *
#*                                                                     *
#* This program is distributed in the hope that it will be useful,     *
#* but WITHOUT ANY WARRANTY; without even the implied warranty of      *
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       *
#* GNU Library General Public License for more details.                *
#*                                                                     *
#* You should have received a copy of the GNU Library General Public   *
#* License along with this program; if not, write to the Free Software *
#* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
#* USA                                                                 *
#*                                                                     *
#***********************************************************************
"""
A smart tuple object with type conversion and math functions
"""

import math

from collections.abc import Iterable

from operator import sub as op_sub
from operator import add as op_add
from operator import mul as op_mul

class SmartTuple():
    """
    A smart tuple object with type conversion and math functions
    """

    _sub = lambda lhs, rhs: tuple(map(op_sub, lhs, rhs))
    _add = lambda lhs, rhs: tuple(map(op_add, lhs, rhs))
    _mul = lambda lhs, rhs: tuple(map(op_mul, lhs, rhs))
    _scl = lambda tpl, scl: tuple([_v * scl for _v in tpl])

    _length = \
        lambda tpl: math.sqrt(tpl[0]*tpl[0] + tpl[1]*tpl[1] + tpl[2]*tpl[2])

    def __init__(self, data):
        """
        Constructor
        """

        self._tuple = tuple(data)

    @staticmethod
    def from_values(*args):
        """
        Build tuple from individual values
        """

        _type = None
        _vals = []

        for _v in args:

            if not _type:

                if isinstance(_v, (int, float)):
                    _type = type(_v)

                elif isinstance(_v, str):
                    _type = float

            _w = _v

            if not isinstance(_v, _type):
                _w = _type(_v)

            _vals.append(_w)

        assert(len(_vals) == len(args)), 'Value type mismatch.'

        return SmartTuple(_vals)

    def _validate(self, args):
        """
        Accepts a single iterable or multiple floats / ints
        """

        _tpl = ()

        if isinstance(args, Iterable):

            if isinstance(args[0], SmartTuple):
                _tpl = args[0]._tuple

            else:
                _tpl = SmartTuple(args)._tuple

        else:

            try:
                _tpl = SmartTuple(args)._tuple

            except Exception:

                assert(len(args) == len(self._tuple)),\
                    'Length mismatch. {} values expected.'\
                        .format(len(self._tuple))

                _tpl = SmartTuple.from_values(args)._tuple

        return _tpl

    def multiply(self, factor):
        """
        Multiply each element by factor (single value only)
        """

        return SmartTuple._mul(self, (factor,)*len(self._tuple))

    def length(self):
        """
        Tuple-base length / magnitude
        """

        return SmartTuple._length(self._tuple)

    def sub(self, *args):
        """
        Tuple-based subtraction
        """

        _tpl = [self._validate(_v) for _v in args]

        #ingle tuple subtraction
        if _tpl[0] and len(_tpl) == 1:
            return SmartTuple._sub(self._tuple, _tpl[0])

        #multiple tuple subtraction
        return ((SmartTuple._sub(self._tuple, _v),) for _v in _tpl if _v)

    def add(self, *args):
        """
        Tuple-based addition
        """

        _tpl = [self._validate(_v) for _v in args]

        #ingle tuple subtraction
        if _tpl[0] and len(_tpl) == 1:
            return SmartTuple._add(self._tuple, _tpl[0])

        #multiple tuple subtraction
        return ((SmartTuple._add(self._tuple, _v),) for _v in _tpl if _v)

    def __add__(self, other):

        self.add(other)

    def __sub__(self, other):

        self.sub(other)

    def __str__(self):

        return str(self._tuple)

    def __repr__(self):

        return self._tuple
