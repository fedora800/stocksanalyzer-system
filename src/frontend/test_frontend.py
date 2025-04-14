import os
import unittest
from unittest.mock import patch

# Import the Streamlit app (frontend.py)
import frontend

class TestFrontend(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.environ')
    def test_environment_detection_docker(self, mock_environ, mock_path_exists):
        """Test if the app correctly detects Docker environment."""
        mock_path_exists.return_value = True
        mock_environ.get.return_value = None
        self.assertEqual(frontend.get_environment(), 'Docker')

    @patch('os.path.exists')
    @patch('os.environ')
    def test_environment_detection_kubernetes(self, mock_environ, mock_path_exists):
        """Test if the app correctly detects Kubernetes environment."""
        mock_path_exists.return_value = False
        mock_environ.get.return_value = 'kubernetes'
        self.assertEqual(frontend.get_environment(), 'Kubernetes')

    @patch('os.path.exists')
    @patch('os.environ')
    def test_environment_detection_unknown(self, mock_environ, mock_path_exists):
        """Test if the app correctly handles unknown environments."""
        mock_path_exists.return_value = False
        mock_environ.get.return_value = None
        self.assertEqual(frontend.get_environment(), 'Unknown')

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestFrontend))