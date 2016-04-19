#! /usr/bin/python

"""
Module contains the answers to the network generated.

AUTHOR:    T.WINN
CREATED:   16 April 2016
MODIFIED:
VERSION:   1.0
"""

# THIRD PARTY IMPORTS
from netaddr import IPNetwork


class Answer(object):
    """
    Class which contains the details of the network which has been
    generated.
    """

    def __init__(self, in_host):
        """
        Initialise an instance of Answer.

        @type in_host: str
        @param in_host: Network in the format of v.x.y.z/c
        """
        self.in_host = IPNetwork(in_host)

        self.network = str(self.in_host.network)
        self.broadcast = str(self.in_host.broadcast)
        self.netmask = str(self.in_host.netmask)
        self.num_hosts = self.in_host.size
        self.usable_hosts = str(self.num_hosts - 2)
