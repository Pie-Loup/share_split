import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manage_seed import create_share_from_seed, rebuild_seed_from_shares
from protect_share import encrypt, decrypt
from sss_helper import get_key_choice, secure_clear, show_qr_code

class TestSeedSplitting(unittest.TestCase):
    def setUp(self):
        self.test_seed = "This is a test seed phrase for unit testing and it is perfectly valid"
        self.test_shares = [
            "053affb5392a18838c6ef2d94d8ebfdaef433ab6cda263ddb4e678469e5181bbce74f2ea77f7e5fe6a62c17f4240eccd91eae065ee7fa237de8695f9849dfd13bcde42a85cb92348788bb341eda4e3d8a88a00b77257eaf330ef1b35ff38c0477191df0666cd6495979f0c76421475ce2e7b1ca21acdb66457d4962b25557d2b03cfb676086e770752501d280e2af902da0db67fae9c2b5fcad776684d40d26fcd231739e252e10af9670a3400cf32ea65bd75bd91d8515c812bbd4381db27392fa557e5a9d7d7dcda37ee3e2bfd83cc248e77cd6f242a4fdcd9757ad7b72184dfa49375e96f7f394edbd7f0e659bb6287fc8bf54edce17e73577b748ef3420c52355b66c5031cc760f62573bb48f5170ce8c60d",
            "10575421", # simulate lost share
            "07b0ff1fab7e498aa54cd88be8ac3f90cdc9b02468e72b991eb368d3daf485336b5ed8bf67e7b1fb3f28447dc6c2c668b5c0a131cb7ee6a79b93c1ec8dd9f73b369ac7f9162b69d969a319c5c8eeab89f99e02265707c0d992cd51a1fdaa40d654b59d1334682dc0c6dd2562c63d616a8b7155e65069232d077dc281700077810b6f2362194b6515f6f057782a80eb088e29237f0bd4821f60866338e7c2774f676945ada6f8a320ec351e9c026d98bf31386138b588f415838337ca859175ab8ef007b0fd8787968ea7caba83f836bb9cd881277a863e2d55a395899ee47dc3d4257980eb69bac52252baf3cecc474ac50d62f721afbba87d38319ad01185520e5f3f4e0e288b715617a97258e89e5863e17f60"
        ]
        self.test_password = "testpassword123"
        self.encrypted_share = encrypt(self.test_password, self.test_shares[0])

    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_create_shares(self, mock_input, mock_getpass):
        # Setup mocks
        mock_input.side_effect = ["2", "3"]  # required_shares, total_shares
        mock_getpass.return_value = self.test_seed

        # Test share creation
        shares = create_share_from_seed(self.test_seed, 2, 3)
        self.assertIsNotNone(shares)
        self.assertEqual(len(shares), 3)

    @patch('builtins.input')
    def test_rebuild_from_shares(self, mock_input):
        # Setup mocks
        mock_input.side_effect = ["2", "3"]  # required_shares, max_shares

        # Test rebuilding
        seed = rebuild_seed_from_shares(self.test_shares, 2)
        self.assertIsNotNone(seed)

    def test_share_encryption(self):
        # Test encryption with password
        encrypted = encrypt(self.test_password, self.test_shares[0])
        self.assertNotEqual(encrypted, self.test_shares[0])

        # Test decryption with correct password
        decrypted = decrypt(self.test_password, encrypted)
        self.assertEqual(decrypted, self.test_shares[0])

        # Test decryption with wrong password
        with self.assertRaises(Exception):
            decrypt("wrongpassword", encrypted)

        # Test empty password
        unencrypted = encrypt("", self.test_shares[0])
        self.assertEqual(unencrypted, self.test_shares[0])

    @patch('sys.stdin')
    @patch('termios.tcgetattr')
    @patch('termios.tcsetattr')
    def test_get_key_choice(self, mock_tcsetattr, mock_tcgetattr, mock_stdin):
        # Test key choice
        mock_stdin.fileno.return_value = 0
        mock_stdin.read.return_value = 'y'
        mock_tcgetattr.return_value = None

        result = get_key_choice(['y'], ['n'])
        self.assertEqual(result, 1)

    @patch('os.system')
    @patch('sys.stdout')
    def test_secure_clear(self, mock_stdout, mock_system):
        # Test terminal clearing
        secure_clear()
        mock_system.assert_called_with('clear || cls || :')

    @patch('qrcode.QRCode')
    def test_show_qr(self, mock_qr):
        # Test QR code display
        mock_qr_instance = MagicMock()
        mock_qr.return_value = mock_qr_instance
        
        show_qr_code("test data")
        mock_qr_instance.add_data.assert_called_with("test data")
        mock_qr_instance.make.assert_called_once()
        mock_qr_instance.print_ascii.assert_called_once()

if __name__ == '__main__':
    unittest.main()
