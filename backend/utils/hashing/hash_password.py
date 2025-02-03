from dataclasses import dataclass
from functools import lru_cache
from argon2 import PasswordHasher, Type
from argon2.exceptions import HashingError, VerifyMismatchError, InvalidHashError
from secrets import token_bytes


@dataclass(frozen=True)
class Argon2Config:
    """Immutable configuration for Argon2 hashing."""
    time_cost: int=3                # Number of iterations
    memory_cost: int=63556          # 64 MB memory usage (KiB)
    parallelism: int=4              # Number of parallel threads
    salt_len: int=16                # Salt length
    algorithm_type: Type=Type.ID    # Argon2 algorithm variant

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


def hash_password(password:str)-> str:
    """Hash a password using Argon2 configurations."""
    config= get_argon_config()
    try:
        return config.hasher.hash(password.encode(), salt=token_bytes(config.salt_len))
    except HashingError as hash_error:
        raise ValueError(f'Password hashing failed: {str(hash_error)}')

def verify_password(password:str, hashed:str)-> bool:
    """Verifies a password against an Argon2 hash."""
    config= get_argon_config()
    try:
        return config.hasher.verify(hashed, password.encode())
    except VerifyMismatchError:
        return False
    except InvalidHashError as invalid_hash:
        # Log invalid hash format
        raise ValueError(f'Invalid hash format: {str(invalid_hash)}')

def needs_rehash(hashed:str)-> bool:
    """Checks if Argon2 hash needs to be re-hashed."""
    config= get_argon_config()
    return config.hasher.check_needs_rehash(hashed)