import base64
import unittest

from cryptography.hazmat.primitives.asymmetric import padding

from app.api.auth.login import resolve_login_password
from app.utils.rsa import private_key


class LoginPasswordResolutionTests(unittest.TestCase):
    def test_plaintext_password_is_kept_as_is(self):
        self.assertEqual(resolve_login_password("12345678"), "12345678")

    def test_rsa_encrypted_password_is_decrypted(self):
        public_key = private_key.public_key()

        ciphertext = public_key.encrypt(
            b"12345678",
            padding.PKCS1v15(),
        )
        encoded = base64.b64encode(ciphertext).decode()

        self.assertEqual(resolve_login_password(encoded), "12345678")


if __name__ == "__main__":
    unittest.main()
