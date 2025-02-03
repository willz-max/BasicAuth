import re
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, DateTime, Integer, func


def camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_ ', name).lower()

class BaseModel:
    @declared_attr
    def __tablename__(self):
        """
        Automatically generates a table name in snake case based on the class name.
        """
        return camel_to_snake(self.__name__)

    id= Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at= Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at= Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    deleted_at= Column(DateTime(timezone=True), nullable=True)

    def save(self, session):
        """
        Automatically handles the session commit or rolls back if necessary.
        Saves the current instance of the model to the database.
        """
        try:
            session.add(self)
            session.commit()
        except Exception as exc:
            raise exc

    def soft_delete(self, session):
        """
        Disables temporarily current instance of the model from database.
        """
        try:
            self.deleted_at= func.now()
            session.commit()
        except Exception as exc:
            raise exc

    def __repr__(self):
        return f'<{self.__class__.__name__}(id={self.id})>'