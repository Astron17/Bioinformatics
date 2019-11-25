import unittest
import bio_info


class Test_Bio_Info(unittest.TestCase):
    def test_Find_All_Paths(self):

        result = len(bio_info.ARRANGMENTS)
        if(len(bio_info.Sequence_1) == 3 and len(bio_info.Sequence_2) == 3):
            self.assertEqual(result, 1)
        if(len(bio_info.Sequence_1) == 7 and len(bio_info.Sequence_2) == 9):
            self.assertEqual(result, 2)
        if(len(bio_info.Sequence_1) == 20 and len(bio_info.Sequence_2) == 20):
            self.assertEqual(result, 3)
        if(len(bio_info.Sequence_1) == 4 and len(bio_info.Sequence_2) == 6):
            self.assertEqual(result, 4)

    def test_score(self):
        sc = bio_info.ARRANGMENTS[0][3][0][1]
        if(len(bio_info.Sequence_1) == 3 and len(bio_info.Sequence_2) == 3):
            self.assertEqual(sc, 1)
        if(len(bio_info.Sequence_1) == 7 and len(bio_info.Sequence_2) == 9):
            self.assertEqual(sc, -3)
        if(len(bio_info.Sequence_1) == 20 and len(bio_info.Sequence_2) == 20):
            self.assertEqual(sc, -3)
        if(len(bio_info.Sequence_1) == 4 and len(bio_info.Sequence_2) == 6):
            self.assertEqual(sc, -2)
