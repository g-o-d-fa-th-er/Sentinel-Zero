import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from main import main

class TestUpdatedSystem(unittest.TestCase):
    @patch('builtins.input', side_effect=['5']) # Simulate entering '5' packets
    @patch('matplotlib.pyplot.savefig') # Mock savefig to avoid file creation during test
    def test_main_flow(self, mock_savefig, mock_input):
        print("Running updated system verification...")
        try:
            main()
            print("System verification successful!")
        except Exception as e:
            self.fail(f"System crashed with error: {e}")

if __name__ == '__main__':
    unittest.main()
