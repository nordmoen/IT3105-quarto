#!/usr/bin/python

import unittest
from board import Board, PlaceTakenError
from piece import Piece

class TestQuartoBoard(unittest.TestCase):

    def setUp(self):
        self.b1 = Board()
    
    def test_place(self):
        self.b1.place(Piece(), 0, 0)
        with self.assertRaises(PlaceTakenError):
            self.b1.place(Piece(), 0, 0)

    def test_get(self):
        self.assertEqual(None, self.b1.get(0, 0))
        self.b1.place(Piece(), 0, 0)
        self.assertEqual(Piece(), self.b1.get(0, 0))
        self.b1.place(Piece(False), 0, 1)
        self.assertEqual(self.b1.get(0, 0), self.b1.get(0, 1))
        self.b1.place(Piece(True, False, False, False), 0, 2)
        self.assertNotEqual(self.b1.get(0, 1), self.b1.get(0, 2))

    def test_col_victory(self):
        self.assertIsNone(self.b1.check_victory((0,0)), None)
        self.b1.place(Piece(), 0, 0)
        self.b1.place(Piece(), 0, 1)
        self.b1.place(Piece(), 0, 2)
        for i in range(4):
            self.assertIsNone(self.b1.check_victory((0, i)))
        self.b1.place(Piece(), 0, 3)
        for i in range(4):
            self.assertIsNotNone(self.b1.check_victory((0, i)))

    def test_row_victory(self):
        self.assertIsNone(self.b1.check_victory((0,0)), None)
        self.b1.place(Piece(), 0, 0)
        self.b1.place(Piece(), 1, 0)
        self.b1.place(Piece(), 2, 0)
        for i in range(4):
            self.assertIsNone(self.b1.check_victory((i, 0)))
        self.b1.place(Piece(), 3, 0)
        for i in range(4):
            self.assertIsNotNone(self.b1.check_victory((i, 0)))

    def test_cross_victory(self):
        self.assertIsNone(self.b1.check_victory((0,0)), None)
        self.b1.place(Piece(), 0, 0)
        self.b1.place(Piece(), 1, 1)
        self.b1.place(Piece(), 2, 2)
        self.b1.place(Piece(), 0, 3)
        for i in range(4):
            self.assertIsNone(self.b1.check_victory((i, i)))
            self.assertIsNone(self.b1.check_victory((i, 3-i)))
        self.b1.place(Piece(), 3,3)
        for i in range(4):
            self.assertIsNotNone(self.b1.check_victory((i, i)))
            self.assertIsNone(self.b1.check_victory((i, 3-i)))

