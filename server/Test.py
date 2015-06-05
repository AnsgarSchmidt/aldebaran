import unittest

class TestSongs(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_helloWorld(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()