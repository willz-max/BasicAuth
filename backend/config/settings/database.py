import os
from functools import lru_cache
from typing import Dict, List, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from modules.shared.base_model import BaseModel

load_dotenv()
Base= declarative_base(cls=BaseModel)

class DatabaseConfig:
    """Database PostgreSQL configurations."""
    def __init__(self):
        self.pg_user= os.environ.get('DB_USER')
        self.pg_pswd= os.environ.get('DB_PASSWORD')
        self.pg_host= os.environ.get('DB_HOST')
        self.pg_port= os.environ.get('DB_PORT')
        self.pg_db= os.environ.get('DB_NAME')

        self._validate_environ()

    @staticmethod
    def _validate_environ()->None:
        required=[
            'DB_USER',
            'DB_PASSWORD',
            'DB_HOST',
            'DB_PORT',
            'DB_NAME',
        ]
        missing_var= [var for var in required if not os.environ.get(var)]
        if missing_var:
            raise ValueError(
                f'Missing required environment variable: {', '.join(missing_var)}'
            )

    @property
    def postgresql_url(self)-> str:
        """PostgreSQL database URI."""
        return (f'postgresql://{self.pg_user}:{self.pg_pswd}@'
                f'{self.pg_host}:{self.pg_port}/{self.pg_db}')

    @property
    def django_db_config(self)-> Dict[str, Dict[str, Any]]:
        """Default Django database configurations."""
        return {
            'default':{
                'ENGINE':'django.db.backends.postgresql',
                'NAME':self.pg_db,
                'USER':self.pg_user,
                'PASSWORD':self.pg_pswd,
                'HOST':self.pg_host,
                'PORT':self.pg_port,
                'CONN_MAX_AGE':600,
                'OPTIONS':{
                    'connect_timeout':10,
                    'sslmode':'require',
                }
            }
        }


@lru_cache()
def postgresql_config()-> DatabaseConfig:
    """Cached instance of configurations for faster retrieval."""
    return DatabaseConfig()

_config= postgresql_config()
_engine= create_engine(_config.postgresql_url)

def get_engine():
    return _engine

def init_postgresql()-> sessionmaker:
    """Initializes PostgreSQL with set configurations."""
    Base.metadata.create_all(bind=_engine)
    return sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=_engine,
    )


#--------------
# EXPORTS
#--------------

SessionLocal= init_postgresql()