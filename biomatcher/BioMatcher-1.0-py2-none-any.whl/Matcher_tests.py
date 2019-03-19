import Matcher
import unittest


class TestMatch(unittest.TestCase):
    def test_positions(self):
        # POS_01
        self.assertTrue(Matcher.match("ACGUACGU", "ACGUACGU", 0, 1, 0, 1))
        # POS_02
        self.assertFalse(Matcher.match("ACGUACGU", "UCGUACGU", 0, 1, 0, 1))
        # POS_03
        self.assertTrue(Matcher.match("ACGUACGU", "ACGUACGU", 0, 7, 0, 7))
        # POS_04
        self.assertFalse(Matcher.match("ACGUACGU", "ACAAACGU", 0, 7, 0, 7))
        # POS_05
        self.assertTrue(Matcher.match("ACGUACGU", "ACGUACGU", 6, 7, 6, 7))
        # POS_06
        self.assertFalse(Matcher.match("ACGUACGU", "ACGUACGA", 6, 7, 6, 7))
        # POS_07
        self.assertTrue(Matcher.match("ACGUACGU", "ACGUACGU", 3, 4, 3, 4))
        # POS_08
        self.assertFalse(Matcher.match("ACGUACGU", "ACGUUCGU", 3, 4, 3, 4))

        # POS_09
        self.assertTrue(Matcher.match("ACGUACGU", "ACGUACGUUUUUUU", 0, 7, 0, 7))
        # POS_10
        self.assertFalse(Matcher.match("ACGUACGU", "ACAAACGUGGGGG", 0, 7, 0, 7))

        # POS_11
        self.assertTrue(Matcher.match("GG", "GG", 0, 1, 0, 1))
        # POS_12
        self.assertFalse(Matcher.match("AU", "UU", 0, 1, 0, 1))
        # POS_13
        self.assertFalse(Matcher.match("GC", "CG", 0, 1, 0, 1))

    def test_efficiency(self):
        # FILE_01
        file1 = open("equal_strings.txt", "r")
        text1 = file1.read()
        line1 = text1.split("\n")
        file2 = open("equal_strings_2.txt", "r")
        text2 = file2.read()
        line2 = text2.split("\n")

        count = 0
        for i in range(0, len(line1)):
            for j in range(0, len(line2)):
                if Matcher.match(line1[i], line2[j], 1, 7, 1, 7):
                    count += 1

        file1.close()
        file2.close()
        self.assertEqual(count, 1000000)

        # FILE_02
        file1 = open("equal_strings.txt", "r")
        text1 = file1.read()
        line1 = text1.split("\n")
        file2 = open("other_strings.txt", "r")
        text2 = file2.read()
        line2 = text2.split("\n")

        count = 0
        for i in range(0, len(line1)):
            for j in range(0, len(line2)):
                if Matcher.match(line1[i], line2[j], 1, 7, 1, 7):
                    count += 1

        file1.close()
        file2.close()
        self.assertEqual(count, 0)

    def test_file(self):
        # FILE_03
        file1 = open("5_strings.txt", "r")
        text1 = file1.read()
        line1 = text1.split("\n")
        file2 = open("6_strings.txt", "r")
        text2 = file2.read()
        line2 = text2.split("\n")

        count = 0
        for i in range(0, len(line1)):
            for j in range(0, len(line2)):
                count += 1

        file1.close()
        file2.close()
        self.assertEqual(count, 30)

        # FILE_04
        file1 = open("5_strings.txt", "r")
        text1 = file1.read()
        line1 = text1.split("\n")
        file2 = open("4_strings.txt", "r")
        text2 = file2.read()
        line2 = text2.split("\n")

        count = 0
        for i in range(0, len(line1)):
            for j in range(0, len(line2)):
                count += 1

        file1.close()
        file2.close()
        self.assertEqual(count, 20)

    def test_compar28(self):
        # CP28_01: Equal strings
        self.assertTrue(Matcher.match("ACGCGCGCAAAAAAAAAAAA", "ACGCGCGCAAAAAAAAAAAA", 1, 7, 1, 7))
        # CP28_02: Equal seed
        self.assertTrue(Matcher.match("ACGCGCGCAAAAAAAAAAAA", "UCGCGCGCUUUUUUUUUUUU", 1, 7, 1, 7))
        # CP28_03: First position error
        self.assertFalse(Matcher.match("AAGCGCGCAAAAAAAAAAAA", "UCGCGCGCUUUUUUUUUUUU", 1, 7, 1, 7))
        # CP28_04: Middle position error
        self.assertFalse(Matcher.match("ACGCACGCAAAAAAAAAAAA", "UCGCGCGCUUUUUUUUUUUU", 1, 7, 1, 7))
        # CP28_05: Last position error
        self.assertFalse(Matcher.match("ACGCGCGAAAAAAAAAAAAA", "UCGCGCGCUUUUUUUUUUUU", 1, 7, 1, 7))

    def test_compar27(self):
        # CP27_01: Equal strings
        self.assertTrue(Matcher.match("ACGCGCGAAAAAAAAAAAAA", "ACGCGCGAAAAAAAAAAAAA", 1, 6, 1, 6))
        # CP27_02: Equal seed
        self.assertTrue(Matcher.match("ACGCGCGAAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 1, 6, 1, 6))
        # CP27_03: First position error
        self.assertFalse(Matcher.match("AAGCGCGCAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 1, 6, 1, 6))
        # CP27_04: Middle position error
        self.assertFalse(Matcher.match("ACGCACGAAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 1, 6, 1, 6))
        # CP27_05: Last position error
        self.assertFalse(Matcher.match("ACGCGCAAAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 1, 6, 1, 6))

    def test_compar38(self):
        # CP38_01: Equal strings
        self.assertTrue(Matcher.match("AACGCGCGAAAAAAAAAAAA", "AACGCGCGAAAAAAAAAAAA", 2, 7, 2, 7))
        # CP38_02: Equal seed
        self.assertTrue(Matcher.match("AACGCGCGAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 2, 7, 2, 7))
        # CP38_03: First position error
        self.assertFalse(Matcher.match("AAACGCGCAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 2, 7, 2, 7))
        # CP38_04: Middle position error
        self.assertFalse(Matcher.match("AACGAGCGAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 2, 7, 2, 7))
        # CP38_05: Last position error
        self.assertFalse(Matcher.match("ACGCGCAAAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 2, 7, 2, 7))

    def test_comparsl27(self):
        # SL27_01: Equal strings slided
        self.assertTrue(Matcher.match("ACGCGCGAAAAAAAAAAAAA", "AACGCGCGAAAAAAAAAAAA", 1, 6, 2, 7))
        # SL27_02: Equal seed slided
        self.assertTrue(Matcher.match("ACGCGCGAAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 1, 6, 2, 7))
        # SL27_03: First position error
        self.assertFalse(Matcher.match("AAGCGCGAAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 1, 6, 2, 7))
        # SL27_04: Middle position error
        self.assertFalse(Matcher.match("ACGCACGAAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 1, 6, 2, 7))
        # SL27_05: Last position error
        self.assertFalse(Matcher.match("ACGCGCAAAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 1, 6, 2, 7))
        # Equal strings not slided(uncertain)
        # self.assertFalse(Match.match("ACGCGCGAAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 1, 6, 2, 7))

    def test_comparsl38(self):
        # SL27_01: Equal strings slided
        self.assertTrue(Matcher.match("AACGCGCGAAAAAAAAAAAA", "ACGCGCGAAAAAAAAAAAAA", 2, 7, 1, 6))
        # SL27_02: Equal seed slided
        self.assertTrue(Matcher.match("AACGCGCGAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 2, 7, 1, 6))
        # SL27_03: First position error
        self.assertFalse(Matcher.match("AAAGCGCGAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 2, 7, 1, 6))
        # SL27_04: Middle position error
        self.assertFalse(Matcher.match("AACGCACGAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 2, 7, 1, 6))
        # SL27_05: Last position error
        self.assertFalse(Matcher.match("AACGCGCAAAAAAAAAAAAA", "UCGCGCGUUUUUUUUUUUUU", 2, 7, 1, 6))
        # Equal strings not slided(uncertain)
        # self.assertFalse(Match.match("AACGCGCGAAAAAAAAAAAA", "UUCGCGCGUUUUUUUUUUUU", 2, 7, 1, 6))

    def test_other(self):
        # 2-8 True -> 2-7 & 3-8 True
        compar28 = (Matcher.match("ACUGCAUCGACGAUGACUGCU", "ACUGCAUCGACGAUGACUGCU", 1, 7, 1, 7))
        compar27 = (Matcher.match("ACUGCAUCGACGAUGACUGCU", "ACUGCAUCGACGAUGACUGCU", 1, 6, 1, 6))
        compar38 = (Matcher.match("ACUGCAUCGACGAUGACUGCU", "ACUGCAUCGACGAUGACUGCU", 2, 7, 2, 7))
        self.assertTrue((not compar28) or compar27 or compar38)

        # 2-8 False -> 2-7 True
        compar28 = (Matcher.match("CAUAUAUUGCGCGCGCGCGCG", "CAUAUAUGGCGCGCGCGCGCG", 1, 7, 1, 7))
        compar27 = (Matcher.match("CAUAUAUUGCGCGCGCGCGCG", "CAUAUAUGGCGCGCGCGCGCG", 1, 6, 1, 6))
        self.assertTrue((not compar28) or compar27)

        # 2-8 False -> 3-8 True
        compar28 = (Matcher.match("CCUAUAUUGCGCGCGCGCGCG", "CAUAUAUUGCGCGCGCGCGCG", 1, 7, 1, 7))
        compar38 = (Matcher.match("CCUAUAUUGCGCGCGCGCGCG", "CAUAUAUUGCGCGCGCGCGCG", 2, 7, 2, 7))
        self.assertTrue((not compar28) or compar38)


if __name__ == '__main__':
    # verbosity=2 for more details in console
    unittest.main(verbosity=2)
