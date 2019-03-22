# -*- coding: utf-8 -*-

import unittest
import pysfish as sf

FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[HEhe] w KQBCDFGkqbcdfg - 0 1"

DATA = {
    "k7/8/8/8/8/8/8/K7 w - - 0 1": (True, True),  # K vs K
    "k7/b7/8/8/8/8/8/K7 w - - 0 1": (True, True),  # K vs KB
    "k7/n7/8/8/8/8/8/K7 w - - 0 1": (True, True),  # K vs KN
    "k7/p7/8/8/8/8/8/K7 w - - 0 1": (True, False),  # K vs KP
    "k7/r7/8/8/8/8/8/K7 w - - 0 1": (True, False),  # K vs KR
    "k7/q7/8/8/8/8/8/K7 w - - 0 1": (True, False),  # K vs KQ
    "k7/nn6/8/8/8/8/8/K7 w - - 0 1": (True, False),  # K vsNN K
    "k7/bb6/8/8/8/8/8/K7 w - - 0 1": (True, False),  # K vs KBB opp color
    "k7/b1b5/8/8/8/8/8/K7 w - - 0 1": (True, True),  # K vs KBB same color
    # TODO: implement more lichess/python-chess adjudication rule
    #    "kb6/8/8/8/8/8/8/K1B6 w - - 0 1": (True, True),  # KB vs KB same color
    #    "kb6/8/8/8/8/8/8/KB7 w - - 0 1": (False, False),  # KB vs KB opp color
}


class TestPysfish(unittest.TestCase):
    def test_info(self):
        result = sf.info()
        self.assertEqual(result[:9], "Stockfish")

    def test_set_option(self):
        result = sf.set_option("UCI_Variant", "seirawan")
        self.assertIsNone(result)

    def test_legal_moves(self):
        fen = "8/8/8/8/8/k7/8/K7 w - - 0 1"
        result = sf.legal_moves(fen, [])
        self.assertEqual(result, ["a1b1"])

    def test_get_fen(self):
        result = sf.get_fen(FEN, [])
        self.assertEqual(result, FEN)

    def test_gives_check(self):
        self.assertRaises(ValueError, sf.gives_check, FEN, [])

        result = sf.gives_check(FEN, ["e2e4"])
        self.assertFalse(result)

        moves = ["f2f3", "e7e5", "g2g4", "d8h4"]
        result = sf.gives_check(FEN, moves)
        self.assertTrue(result)

    def test_is_optional_game_end(self):
        result = sf.is_optional_game_end(FEN, [])
        self.assertNotEqual(result, 0)

    def test_has_insufficient_material(self):
        for fen in DATA:
            # print(fen, standard[fen])
            result = sf.has_insufficient_material(fen, [])
            self.assertEqual(result, DATA[fen])


if __name__ == '__main__':
    unittest.main()
