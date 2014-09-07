#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Alfred
#
# Created:     12/12/2012
# Copyright:   (c) Alfred 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import unittest
from TileMill import TileMill

class TileMillTestCase(unittest.TestCase):
    '''
    '''

    def test_constructor(self):
        tm = TileMill(r'C:\Program Files (x86)\TileMill-v0.10.1\tilemill')

