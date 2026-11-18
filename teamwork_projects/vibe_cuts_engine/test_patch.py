import unittest
from unittest.mock import patch

class MyClass:
    pass

class Test(unittest.TestCase):
    @patch('__main__.MyClass.does_not_exist')
    def test_mock(self, mock_obj):
        pass

if __name__ == '__main__':
    unittest.main()
