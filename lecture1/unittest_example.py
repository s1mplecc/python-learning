import unittest
from vector import Vector


class UnitTest(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FbOO')

    def test_ss(self):
        v = Vector()

        self.assertEqual(str(v), 'Vector(0,)')


if __name__ == "__main__":
    unittest.main()
