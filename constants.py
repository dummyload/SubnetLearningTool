#! /usr/bin/python

"""
Module containing constant values to be used throughout the utility.

AUTHOR:    T.WINN
CREATED:   16 April 2016
MODIFIED:
VERSION:   1.0
"""

#######################################################################
#                       NETWORK CLASS CONSTANTS                       #
#######################################################################
CLASS_A_LOWER_OCTET = 1
CLASS_A_UPPER_OCTET = 127
CLASS_A_LOWER_CIDR = 8
CLASS_A_RESERVED = [127]

CLASS_B_LOWER_OCTET = 128
CLASS_B_UPPER_OCTET = 191
CLASS_B_LOWER_CIDR = 16
CLASS_B_RESERVED = [169]

CLASS_C_LOWER_OCTET = 192
CLASS_C_UPPER_OCTET = 223
CLASS_C_LOWER_CIDR = 24
CLASS_C_RESERVED = []

LOWER_OCTET_VALUE = 0
UPPER_OCTET_VALUE = 255

UPPER_CIDR_VALUE = 30


#######################################################################
#                                FILES                                #
#######################################################################
SETTINGS_FILE = "settings.txt"
