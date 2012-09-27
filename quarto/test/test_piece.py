#!/usr/bin/python

import unittest
from piece import Piece

class TestQuartoPiece(unittest.TestCase):

    def setUp(self):
        self.p1 = Piece()
        self.p2 = Piece(False)
        self.p3 = Piece(tall=False)
        self.p4 = Piece(square=False)
        self.p5 = Piece(hollow=False)
        self.p6 = Piece(False, False, False, False)
        self.all = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]

    def test_eq(self):
        for piece in self.all[1:]:
            self.assertTrue(piece == self.p6)
        for piece in self.all[:-1]:
            self.assertTrue(piece == self.p1)
        self.assertFalse(self.p1 == self.p6)

    def test_str(self):
        self.assertEquals(str(self.p1), '[D*]')
        self.assertEquals(str(self.p2), '[L*]')
        self.assertEquals(str(self.p3), '[d*]')
        self.assertEquals(str(self.p4), '(D*)')
        self.assertEquals(str(self.p5), '[D]')
        self.assertEquals(str(self.p6), '(l)')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestQuartoPiece))
    return suite

if __name__ == '__main__':
        unittest.main()            
