"""
Unit tests for the Pawn class.
"""
import sys
import unittest
sys.path.append("pieces/")
from pawn import Pawn
from exceptions import InvalidMove

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.white_pawn = Pawn((0, 1), "White")
        self.black_pawn = Pawn((0, 6), "Black")
    
    def test_move_valid(self):
        self.white_pawn.move((0, 2))
        self.assertEqual(self.white_pawn.coords, (0, 2))
        
        self.black_pawn.move((0, 5))
        self.assertEqual(self.black_pawn.coords, (0, 5))
    
    def test_move_invalid(self):
        with self.assertRaises(InvalidMove):
            self.white_pawn.move((0, 3))
        
        with self.assertRaises(InvalidMove):
            self.black_pawn.move((0, 4))
    
    def test_get_valid_moves(self):
        self.assertEqual(self.white_pawn.get_valid_moves(), [(0, 2), (0, 3)])
        self.assertEqual(self.black_pawn.get_valid_moves(), [(0, 5), (0, 4)])
    

test = TestPawn()
test.setUp()
test.test_move_valid()
test.test_move_invalid()
test.test_get_valid_moves()
print("All tests passed!")