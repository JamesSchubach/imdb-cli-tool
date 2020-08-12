import unittest
import unittest.mock
from unittest.mock import patch, call
import main
import filecmp


class TestIMDB(unittest.TestCase):
    def testReverseList(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = main.reverseList(data, True)
        self.assertEqual(result, data)
        result = main.reverseList(data, False)
        self.assertEqual(result, [3, 2, 1])

    @patch('builtins.input', side_effect=['t-j'])
    def testGetActorName(self, input_mock):
        expected = [call("\nHello, Please enter the Movie Stars Name: ")]
        name = main.getActorName()
        self.assertEqual(name, "t-j")

    def testGetActors(self):
        actors = main.getActors("t-j")
        self.assertTrue(len(actors) > 1)
        actors = main.getActors(",,")
        self.assertFalse(len(actors) > 1)

    @patch('builtins.input', side_effect=['1'])
    def testGetSpecificActor(self, input_mock):
        name = main.getSpecificActor(["Arizona Muse", "Arizona Mai", "Gustavo Arizona Moreno",
                                      "Arizona Sonora Desert Museum", "Northern Arizona", "Meteor Crater"])
        self.assertEqual(name, "Arizona Muse")

    def testGetMovies(self):
        movies = main.getMovies(('T.J. Mackenzie', '/name/nm1648278/'), True)
        self.assertEqual(movies["movies"], [
                         "A Song from the Heart", "Breaker High"])

    def testGetMovies2(self):
        movies = main.getMovies(('T.J. Mackenzie', '/name/nm1648278/'), False)
        self.assertEqual(movies["movies"], [
                         "Breaker High", "A Song from the Heart"])

    @patch('builtins.input', side_effect=['y', 'yes'])
    def testHandleYesNo(self, input_mock):
        answer = main.handleYesNo("test")
        self.assertTrue(answer)

    def testStr2boolTrue(self):
        answer = main.str2bool('yes')
        self.assertTrue(answer)

    def testStr2boolFalse(self):
        answer = main.str2bool('no')
        self.assertFalse(answer)

    def testSendToJson(self):
        actor = ('T.J. Mackenzie', '/name/nm1648278/')
        movies = main.getMovies(actor, True)
        main.sendToJson(actor[0], movies)
        self.assertTrue(filecmp.cmp(
            "./test.json", "./T.J._Mackenzie_movies.json"))


if __name__ == '__main__':
    unittest.main()
