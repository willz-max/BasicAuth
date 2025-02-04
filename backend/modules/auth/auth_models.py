from sqlalchemy import Column, String
from config.settings.database import Base


class ClientUser(Base):
    """Client user model class."""

    first_name= Column(String(40), nullable=False)
    last_name= Column(String(40), nullable=False)
    email= Column(String(100), unique=True, nullable=False)
    password_hash= Column(String(255), nullable=False)

    def _validate_data(self):
        """Validate data before saving purposes."""
        required={
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'password_hash':self.password_hash
        }
        missing_data= [field for field, value in required.items() if not value]
        if missing_data:
            raise ValueError(
                f'Missing required fields: {', '.join(missing_data)}'
            )

    def __repr__(self):
        return f'<ClientUser: (id:{self.id} | name:{self.first_name} {self.last_name})>'