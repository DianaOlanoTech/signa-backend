from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

# Create the base class that all our database models will inherit from
# This provides common functionality like table mapping and ORM features
Base = declarative_base()


class Trademark(Base):
    """
    Trademark database model representing a trademark record.

    This class defines the structure of the 'trademarks' table in the database.
    Each instance of this class represents a single trademark record.
    """

    # Define the actual table name in the database
    __tablename__ = "trademarks"

    # Primary key column - unique identifier for each trademark
    # autoincrement=True means the database will automatically generate new IDs
    # index=True creates a database index for faster queries on this column
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Trademark name - required field with maximum 100 characters
    # nullable=False means this field cannot be empty
    # index=True creates an index since we'll often search by name
    name = Column(String(100), nullable=False, index=True)

    # Trademark description - optional field for longer text
    # Text type allows for longer descriptions than String
    # nullable=True means this field can be empty
    description = Column(Text, nullable=True)

    # Trademark status - required field with maximum 50 characters
    # default="Active" sets a default value when no status is provided
    status = Column(String(50), nullable=False, default="Active")

    def __repr__(self):
        """
        String representation of the Trademark object.
        This is useful for debugging and logging - shows key information about the object.

        Returns:
            String showing the trademark's ID, name, and status
        """
        return f"<Trademark(id={self.id}, name='{self.name}', status='{self.status}')>"