#!/usr/bin/python

"""
Module containing the class declaration for the address classes.

AUTHOR:    T.WINN
CREATED:   16 April 2016
MODIFIED:
VERSION:   1.0
"""

# STDLIB IMPORTS
import random

# LOCAL IMPORTS
from constants import (CLASS_A_LOWER_OCTET, CLASS_A_UPPER_OCTET, CLASS_A_LOWER_CIDR,
                       CLASS_B_LOWER_OCTET, CLASS_B_UPPER_OCTET, CLASS_B_LOWER_CIDR,
                       CLASS_C_LOWER_OCTET, CLASS_C_UPPER_OCTET, CLASS_C_LOWER_CIDR,
                       CLASS_A_RESERVED, CLASS_B_RESERVED, CLASS_C_RESERVED)


class _NetworkClass(object):
    """

    """

    def __init__(self, lower_first_octet, upper_first_octet, lowest_cidr, reserved_octets):
        """
        Initialise the _AddressClass.

        @type lower_first_octet: int
        @param lower_first_octet: The lower value for a network address
            class.

        @type upper_first_octet: int
        @param upper_first_octet: The upper value for a network address
            class.

        @type lowest_cidr: int
        @param lowest_cidr: Lowest CIDR value for a network class.
            i.e. Class A -> 8 (/8)
                 Class B -> 16 (/16)
                 Class C -> 24 (/24)

        @type reserved_octets: list(int)
        @param reserved_octets: Octets which are reserved and therefore
            cannot be used. i.e. 127 (from 127.0.0.0)
        """
        self.lower_first_octet = int(lower_first_octet)
        self.upper_first_octet = int(upper_first_octet)
        self.lowest_cidr = lowest_cidr
        self.reserved_octets = reserved_octets

    def generate_first_octet(self):
        """
        Generate a random number for the first octet based the range of
        the lower and upper values.

        If the value is in the excluded list, generate a new value.

        @rtype: int
        @return: First octet to be used as a part of the network
            address to be guessed.
        """
        return_var = random.randrange(start=self.lower_first_octet,
                                      stop=self.upper_first_octet+1)

        # ensure that the value returned is not a reserved value.
        while return_var in self.reserved_octets:
            print "in excluded"
            return_var = random.randrange(start=self.lower_first_octet,
                                          stop=self.upper_first_octet+1)

        return return_var


class_a = _NetworkClass(lower_first_octet=CLASS_A_LOWER_OCTET,
                        upper_first_octet=CLASS_A_UPPER_OCTET,
                        lowest_cidr=CLASS_A_LOWER_CIDR,
                        reserved_octets=CLASS_A_RESERVED)

class_b = _NetworkClass(lower_first_octet=CLASS_B_LOWER_OCTET,
                        upper_first_octet=CLASS_B_UPPER_OCTET,
                        lowest_cidr=CLASS_B_LOWER_CIDR,
                        reserved_octets=CLASS_B_RESERVED)

class_c = _NetworkClass(lower_first_octet=CLASS_C_LOWER_OCTET,
                        upper_first_octet=CLASS_C_UPPER_OCTET,
                        lowest_cidr=CLASS_C_LOWER_CIDR,
                        reserved_octets=CLASS_C_RESERVED)
