from contextlib import contextmanager
from config.settings.database import SessionLocal

@contextmanager
def get_db_session():
    """Provide a scoped session with automatic commit, rollback, and close."""
    session= SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()