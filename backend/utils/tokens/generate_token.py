from dataclasses import dataclass
from typing import Dict, Any, Type
import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

@dataclass(frozen=True)
class PayloadModel:
    """Custom interface for payload structure."""
    def __init__(self, **kwargs):
        """Initialize and validate fields."""
        cls= self.__class__
        hints= cls.__annotations__

        for field, field_type in hints.items():
            if field not in kwargs:
                raise ValueError(f'Missing required field: {field}')

            value= kwargs[field]
            if not isinstance(value, field_type):
                raise TypeError(f'Invalid type for {field}: expected {field_type.__name__}, got {type(value.__name__)}')

            setattr(self, field, value)

    def dict(self)->Dict[str, Any]:
        """Convert object to dictionary."""
        return {
            field: getattr(self, field) for field in self.__annotations__
        }

    @classmethod
    def validate(cls:Type['PayloadModel'], data:Dict[str, Any])-> 'PayloadModel':
        """Factory method to create an instance with validation."""
        return cls(**data)

@dataclass(frozen=True)
class PayloadInterface(PayloadModel):
    """Interface for payload structure."""
    sub: str  # Subject (e.g, user_id)
    exp: datetime  # Expiration time
    iat: datetime  # Issued at time


class TokenConfig:
    """Immutable configuration for JWT token generation."""
    def __init__(self):
        self._algorithm:str= 'HS256'
        self._secret_key:str= os.getenv('DJANGO_SECRET_KEY')


    def _validate_environ(self)->None:
        """Validates required environment variables if existing."""
        required=[
            self._secret_key,
        ]
        if [var for var in required if not os.getenv(var)]:
            raise ValueError

    @property
    def secret_key(self)->str:
        """Secure secret key getter with validation."""
        try:
            self._validate_environ()
            return self._secret_key
        except Exception as exc:
            raise exc

    def tokenize(self,payload:PayloadInterface):
        """Standardized tokenizer for encoding payloads."""
        try:
            return jwt.encode(payload.dict(), self._secret_key, self._algorithm)
        except Exception as exc:
            raise exc

    def de_tokenize(self, token:str):
        """Standardized JWT token decoder that verifies if token is valid."""
        try:
            return jwt.decode(
                token,
                self._secret_key,
                self._algorithm
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as exc:
            raise exc


@lru_cache(maxsize=1)
def get_token_config()-> TokenConfig:
    """Returns a single cached instance of TokenConfig."""
    return TokenConfig()

service= get_token_config()


def generate_token(payload_user):
    """Generates a JWT token for authenticated user."""
    payload:dict={
        'sub':payload_user,
        'exp':datetime.datetime.now()+ datetime.timedelta(minutes=15),
        'iat':datetime.datetime.now()
    }
    try:
        _valid_payload= PayloadInterface.validate(payload)
        return service.tokenize(_valid_payload)
    except Exception as exc:
        raise exc

def verify_token(token:str)->str:
    """Verifies the JWT token and returns user data."""
    try:
        return service.de_tokenize(token)
    except Exception as exc:
        raise exc