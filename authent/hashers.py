import bcrypt
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.translation import gettext_noop as _


class NativeBcryptPasswordHasher(BasePasswordHasher):
    """
    Hasher for native bcrypt passwords (without Django prefix).
    Allows Django to verify bcrypt hashes from external applications.

    Works with passwords starting with $2a$, $2b$, $2x$, or $2y$.
    """

    algorithm = "bcrypt_native"

    def encode(self, password, salt):
        """Store a dummy/unusable password for external users.

        Since these users authenticate against an external database,
        we don't need to store their real password in Django.
        """
        # Return an unusable password marker
        return "!"

    def verify(self, password, encoded):
        """Verify password using bcrypt library directly.

        Strips the 'bcrypt_native$' prefix if present, then detects and verifies
        native bcrypt hashes (starting with $2a$, $2b$, $2x$, $2y$).
        """
        print("ENTER LA ???")
        # Strip the hasher prefix if present
        if encoded.startswith("bcrypt_native$"):
            encoded = encoded[len("bcrypt_native$") :]
        # Only handle bcrypt hashes
        if not (
            encoded.startswith("$2a$")
            or encoded.startswith("$2b$")
            or encoded.startswith("$2x$")
            or encoded.startswith("$2y$")
        ):
            return False

        try:
            return bcrypt.checkpw(password.encode(), encoded.encode())
        except (ValueError, TypeError):
            return False

    def safe_summary(self, encoded):
        return {
            _("algorithm"): self.algorithm,
            _("hash"): mask_hash(encoded, show=4),
        }

    def harden_runtime(self, password, encoded):
        pass

    def decode(self, encoded):
        return {
            "algorithm": self.algorithm,
            "hash": encoded,
            "salt": None,
        }
