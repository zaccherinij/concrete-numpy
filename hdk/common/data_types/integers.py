"""This file holds the definitions for integer types"""

import math
from typing import Iterable

from . import base


class Integer(base.BaseDataType):
    """Class representing an integer"""

    bit_width: int
    is_signed: bool

    def __init__(self, bit_width: int, is_signed: bool) -> None:
        assert bit_width > 0, "bit_width must be > 0"
        self.bit_width = bit_width
        self.is_signed = is_signed

    def __repr__(self) -> str:
        signed_str = "signed" if self.is_signed else "unsigned"
        return f"{self.__class__.__name__}<{signed_str}, {self.bit_width} bits>"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.bit_width == other.bit_width
            and self.is_signed == other.is_signed
        )

    def min_value(self) -> int:
        """Minimum value representable by the Integer"""
        if self.is_signed:
            return -(2 ** (self.bit_width - 1))

        return 0

    def max_value(self) -> int:
        """Maximum value representable by the Integer"""
        if self.is_signed:
            return 2 ** (self.bit_width - 1) - 1

        return 2 ** self.bit_width - 1

    def can_represent_value(self, value_to_represent: int) -> bool:
        """A helper function to check if a value is representable by the Integer

        Args:
            value_to_represent (int): Value to check

        Returns:
            bool: True if the value can be represented by this integer
        """
        return self.min_value() <= value_to_represent <= self.max_value()


def create_signed_integer(bit_width: int) -> Integer:
    """Convenience function to create a signed integer

    Args:
        bit_width (int): width of the integer

    Returns:
        Integer: A signed integer with the requested bit_width
    """
    return Integer(bit_width, is_signed=True)


SignedInteger = create_signed_integer


def create_unsigned_integer(bit_width: int) -> Integer:
    """Convenience function to create an unsigned integer

    Args:
        bit_width (int): width of the integer

    Returns:
        Integer: An unsigned integer with the requested bit_width
    """

    return Integer(bit_width, is_signed=False)


UnsignedInteger = create_unsigned_integer


def make_integer_to_hold_ints(values: Iterable[int], force_signed: bool) -> Integer:
    """Returns an Integer able to hold all values, it is possible to force the Integer to be signed

    Args:
        values (Iterable[int]): The values to hold
        force_signed (bool): Set to True to force the result to be a signed Integer

    Returns:
        Integer: The Integer able to hold values
    """
    assert all(isinstance(x, int) for x in values)
    min_value = min(values)
    max_value = max(values)

    make_signed_integer = force_signed or min_value < 0

    num_bits = max(
        get_bits_to_represent_int(min_value, make_signed_integer),
        get_bits_to_represent_int(max_value, make_signed_integer),
    )

    return Integer(num_bits, is_signed=make_signed_integer)


def get_bits_to_represent_int(value: int, force_signed: bool) -> int:
    """Returns how many bits are required to represent a single int

    Args:
        value (int): The int for which we want to know how many bits are required
        force_signed (bool): Set to True to force the result to be a signed Integer

    Returns:
        int: required amount of bits
    """

    # Writing this in a very dumb way
    num_bits: int
    if value < 0:
        abs_value = abs(value)
        if abs_value > 1:
            num_bits = math.ceil(math.log2(abs_value)) + 1
        else:
            # -1 case
            num_bits = 2
    else:
        if value > 1:
            num_bits = math.ceil(math.log2(value + 1))
        else:
            # 0 and 1 case
            num_bits = 1

        if force_signed:
            num_bits += 1

    return num_bits
