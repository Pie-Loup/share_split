import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from bip_utils import Bip44Coins
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manage_seed import create_share_from_seed, rebuild_seed_from_shares
from protect_share import encrypt, decrypt
from sss_helper import get_key_choice, secure_clear, show_qr_code
from seed import generate_address

class TestSeedSplitting(unittest.TestCase):
    def setUp(self):
        self.test_seed =  "track vital video layer announce stage paddle harvest case unit donate surface tail raw draft bag immune sting tent beyond raven fold weird verify"
        self.test_shares = [
            "01789bb58c9b48037c083ca121a78332363dedd7790a03612c54faebef8bd190ad3c6760f65b37a474fed777333f10a4f1b19e1286c025d347188b7b1fadce74e63cf75296f99c706f6d850fc22f552e920e1dbe2a9df97fb968cf14c623bf2fd3dbb6225ca8211a8fc86d77a3badcb379a11cc500cd9994cf025b4ad35075d0e9bfac5edab59aac5ac91847869bcb1c0617415e71e0ac32b9426a2c1723f1722b92208bdd291903a34b1ff3413c9b5b0d486c6f3bc18e08e28bf66882842c150b808893ec19d976001edcd310d71c79cbfe57df69e9f8290ffee1973d52ae49101c50957ba4eaf8147ca9c3ee6f7851f6f28807f026b96a73a1bcc7555c0ee72e2eb0b2d9fa7c2b04b1ff0d2d353bbbd37fda1b",
            "0469d320a5d1d80a7418b5e364f68996a2b9c9866b1e0a2384fef0c3cea374b207b53622e311a6ed5efc866599bd31eed514da3794407179d549a2715f096b5eb2b6e5f7c4ecd5514e488f2f468dff8bb62a593a7fd9ec7f2c3a6d3e526b3d8f7b93226715f8634faf594866eb30961a6ce3564f0268ccbe6d0711e079f16172bcea1c37cd59f9c423886013bb927481497ae5da7cdf11cd47867ba7688ce979bbec20bcaeb87c40a9009d10fadd07d057166060e85dc1d9e0e0fc6f46a1a76c3a40d0dce78aa397bf75ab9465c28ea3231244cb657d03b841bbdbe0f52b229a6b92237fa013e5fd60abbc64e27b8c27a3eecd3ae83367746806598dbf2f69c8bfafd14baf16ac401f4b2a42bf5ec66895acc15f"
        ]
        self.test_password = "testpassword123"
        self.bitcoin_address = "17LRo2XR8yauendAGMqj3DT8zUA3JBYcDc"
        self.ethereum_address = "0xE7d017Fe2208b2f0508A313012A5C9729EE1668e"
        self.passphrase_bitcoin_address = "1K3bfvMx2mQHrQZq7J8ccnAMm2L7i9tgEQ"
        self.passphrase_ethereum_address = "0x8Fa07b64e51A911a5320dB161849988Bc6768910"
        self.encrypted_share = encrypt(self.test_password, self.test_shares[0])

    def test_create_shares(self):

        # Test share creation
        shares = create_share_from_seed(self.test_seed, 2, 3)
        self.assertIsNotNone(shares)
        self.assertEqual(len(shares), 3)

    def test_rebuild_from_shares(self):

        # Test rebuilding
        seed = rebuild_seed_from_shares(self.test_shares, 2)
        self.assertIsNotNone(seed)
        self.assertEqual(seed, self.test_seed)

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

    def test_public_addresses(self):
        # Test public address generation
        self.assertEqual(self.bitcoin_address, generate_address(self.test_seed, Bip44Coins.BITCOIN, ""))
        self.assertEqual(self.ethereum_address, generate_address(self.test_seed, Bip44Coins.ETHEREUM, ""))
        self.assertEqual(self.passphrase_bitcoin_address, generate_address(self.test_seed, Bip44Coins.BITCOIN, self.test_password))
        self.assertEqual(self.passphrase_ethereum_address, generate_address(self.test_seed, Bip44Coins.ETHEREUM, self.test_password))


if __name__ == '__main__':
    unittest.main()
