from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Session
from src.db.base import Trademark
from src.api.v1.schemas.trademarks import TrademarkCreate, TrademarkUpdate

# TYPE_CHECKING is used to avoid circular imports while still providing type hints
if TYPE_CHECKING:
    # Only for type hints, avoids circular import issues
    pass


def get_trademark(db: Session, trademark_id: int) -> Optional[Trademark]:
    """
    Retrieves a single trademark by its unique ID.

    This function queries the database for a trademark with the specified ID.
    """
    # Query the Trademark table, filter by ID, and return the first match
    # .first() returns None if no match is found
    return db.query(Trademark).filter(Trademark.id == trademark_id).first()


def get_trademarks(db: Session, skip: int = 0, limit: int = 100) -> list[Trademark]:
    """
    Retrieves a paginated list of trademarks from the database.

    This function implements pagination to handle large datasets efficiently.
    It skips a specified number of records and limits the results returned.
    """
    # Query all trademarks, apply pagination, and return as list
    # .offset() skips the specified number of records
    # .limit() restricts the number of results returned
    # .all() executes the query and returns all matching records
    return db.query(Trademark).offset(skip).limit(limit).all()


def get_trademarks_count(db: Session) -> int:
    """
    Counts the total number of trademarks in the database.

    This function is useful for pagination calculations and displaying
    total counts in user interfaces.
    """
    # Count all records in the Trademark table
    # .count() returns the number of records matching the query
    return db.query(Trademark).count()


def create_trademark(db: Session, trademark: TrademarkCreate) -> Trademark:
    """
    Creates a new trademark record in the database.

    This function takes a Pydantic schema object, converts it to a SQLAlchemy
    model instance, saves it to the database, and returns the saved object
    with its generated ID.
    """
    # Create a new Trademark model instance from the schema data
    # We explicitly map each field to ensure data integrity
    db_trademark = Trademark(
        name=trademark.name,
        description=trademark.description,
        status=trademark.status
    )

    # Add the new object to the database session
    # This stages the object for insertion but doesn't save it yet
    db.add(db_trademark)

    # Commit the transaction to save the changes to the database
    # This is when the actual INSERT statement is executed
    db.commit()

    # Refresh the object to get the auto-generated ID from the database
    # This ensures our object has the same data as what's stored in the DB
    db.refresh(db_trademark)

    return db_trademark


def update_trademark(db: Session, trademark_id: int, trademark_update: TrademarkUpdate) -> Trademark | None:
    """
    Updates an existing trademark record in the database.

    This function performs a partial update - only the fields provided
    in the update schema will be modified. Other fields remain unchanged.
    """
    # First, find the existing trademark in the database
    db_trademark = db.query(Trademark).filter(Trademark.id == trademark_id).first()

    # If trademark doesn't exist, return None to indicate failure
    if not db_trademark:
        return None

    # Convert the Pydantic update schema to a dictionary
    # exclude_unset=True means only fields that were explicitly set are included
    # This allows for partial updates - unset fields are ignored
    update_data = trademark_update.model_dump(exclude_unset=True)

    # Iterate through the provided update data and apply changes
    # setattr() dynamically sets object attributes
    for field, value in update_data.items():
        setattr(db_trademark, field, value)

    # Commit the changes to the database
    db.commit()

    # Refresh to ensure our object matches the database state
    db.refresh(db_trademark)

    return db_trademark


def delete_trademark(db: Session, trademark_id: int) -> bool:
    """
    Deletes a trademark record from the database.

    This function finds the trademark by ID and removes it from the database.
    It returns a boolean indicating whether the operation was successful.
    """
    # Find the trademark to delete
    db_trademark = db.query(Trademark).filter(Trademark.id == trademark_id).first()

    # If trademark doesn't exist, return False
    if not db_trademark:
        return False

    # Delete the object from the database session
    db.delete(db_trademark)

    # Commit the deletion to the database
    # This is when the actual DELETE statement is executed
    db.commit()

    # Return True to indicate successful deletion
    return True


def search_trademarks_by_name(db: Session, name: str) -> list[Trademark]:
    """
    Searches for trademarks by name using partial, case-insensitive matching.

    This function allows users to find trademarks by typing part of the name.
    The search is case-insensitive, so "nike", "Nike", and "NIKE" will all
    find trademarks containing those letters.
    """
    # Use ilike for case-insensitive partial matching
    # The % symbols are wildcards that match any characters
    # So "%name%" will match any string containing "name" anywhere within it
    return db.query(Trademark).filter(
        Trademark.name.ilike(f"%{name}%")  # ilike = case-insensitive LIKE
    ).all()