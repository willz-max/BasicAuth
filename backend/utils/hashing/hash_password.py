from dataclasses import dataclass
from functools import lru_cache
from argon2 import PasswordHasher, Type
from argon2.exceptions import HashingError, VerifyMismatchError, InvalidHashError
from secrets import token_bytes


@dataclass(frozen=True)
class Argon2Config:
    """Immutable configuration for Argon2 hashing."""
    time_cost: int=3                # Number of iterations (increase to 5 for more security against brute-force attacks)
    memory_cost: int=63556          # 64 MB memory usage (KiB) (increase from 64 to 128Mib for more security against GPU/ASIC based attacks)
    parallelism: int=4              # Number of parallel threads (reduce to 2 on single-core systems)
    salt_len: int=16                # Salt length (recommended)
    algorithm_type: Type=Type.ID    # Argon2 algorithm variant (recommended)

    @property
    def hasher(self)-> PasswordHasher:
        """Cached property for PasswordHasher instance."""
        return PasswordHasher(
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            salt_len=self.salt_len,
            type=self.algorithm_type,
        )


@lru_cache(maxsize=1)
def get_argon_config()-> Argon2Config:
    """Returns a singleton Argon2 configuration instance."""
    return Argon2Config()


def hash_password(
        password:str,
        custom_salt:bytes=None,
        encoding:str='utf-8',
)-> str:
    """
    Hashes a password using Argon2 configurable settings.

    :param password: Password string to be hashed.
    :param custom_salt: Optional pre-generated salt (16-byte recommended).
                        WARNING: For use only for crypto-safe salt generation.
    :param encoding: Codec in which password is to be encoded.

    :returns: Argon2 hash string.

    :raises: HashingError if hashing failure.
    """

    config= get_argon_config()
    try:
        salt= custom_salt if custom_salt else token_bytes(config.salt_len)
        return config.hasher.hash(password.encode(encoding), salt=salt)
    except HashingError as hash_error:
        raise ValueError(f'Password hashing failed: {str(hash_error)}') from hash_error

def verify_password(
        password:str,
        hashed_password:str,
        encoding:str='utf-8',
        return_hash:bool=False,
)-> bool | tuple[bool, str]:
    """
    Verifies a password against an Argon2 hash with additional options.

    :param password: Password string to be verified against Argon2 hash.
    :param hashed_password: Hashed Argon2 string to be verified against.
    :param encoding: Codec for hash verification.
    :param return_hash: If True, returns tuple (success, new_hash) for rehashing.

    :returns: Verification result or tuple with updated hash.
    :raises: InvalidHash for malformed hashes.
    """

    config= get_argon_config()
    try:
        is_valid= config.hasher.verify(hashed_password, password.encode(encoding))
        if return_hash:
            if needs_rehash(hashed_password):
                return is_valid, hash_password(password)
            return is_valid, hashed_password
        return is_valid
    except VerifyMismatchError:
        return (False, hashed_password) if return_hash else False
    except InvalidHashError as invalid_hash:
        # Log invalid hash format
        raise ValueError(f'Invalid hash format: {str(invalid_hash)}')

def needs_rehash(hashed:str)-> bool:
    """
    Checks if Argon2 hash needs to be re-hashed.

    :param hashed: Hashed Argon2 string.
    :returns: True if hashed string fails check | False if check pass.
    """
    config= get_argon_config()
    return config.hasher.check_needs_rehash(hashed)