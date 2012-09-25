#!/usr/bin/python

import unittest
from test import test_piece
from test import test_board

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(test_piece.TestQuartoPiece))
suite.addTest(unittest.makeSuite(test_board.TestQuartoBoard))
unittest.TextTestRunner(verbosity=2).run(suite)
