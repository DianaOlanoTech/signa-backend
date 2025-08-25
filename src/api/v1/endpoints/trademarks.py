from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from src.db.session import get_db
from src.db.base import Trademark
from src.crud import crud_trademark
from src.api.v1.schemas import trademarks as trademark_schemas

# Create an APIRouter instance
# All routes defined here will inherit the configurations we pass when including
# it in main.py (such as the prefix "/api/v1/trademarks" and tags)
# APIRouter allows us to organize related endpoints together and apply common configurations
router = APIRouter()


@router.post("", response_model=trademark_schemas.TrademarkResponse, status_code=status.HTTP_201_CREATED)
def create_trademark(
        trademark: trademark_schemas.TrademarkCreate,  # Request body containing trademark data
        db: Session = Depends(get_db)  # Database session injected as dependency
):
    """
    Create a new trademark in the database.

    This endpoint accepts trademark data and creates a new record.
    It returns the created trademark with its generated ID.
    """
    try:
        # Delegate the creation to our CRUD function
        return crud_trademark.create_trademark(db=db, trademark=trademark)
    except Exception as e:
        # Generic catch for unexpected errors during creation
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating trademark: {str(e)}"
        )


@router.get("", response_model=trademark_schemas.TrademarkListResponse)
def read_trademarks(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve a paginated list of all trademarks.
    This endpoint now returns an object containing the list of trademarks
    for the current page and the total number of records in the database.
    """
    # Get the list of brands for the current page using the existing CRUD function.
    trademarks = crud_trademark.get_trademarks(db, skip=skip, limit=limit)

    # Obtain the total number of brands using the existing CRUD function.
    total = crud_trademark.get_trademarks_count(db)

    # Returns a dictionary that matches the structure of our new "TrademarkListResponse" schema.
    return {"data": trademarks, "total": total}


@router.get("/{trademark_id}", response_model=trademark_schemas.TrademarkResponse)
def read_trademark(
        trademark_id: int,  # Path parameter - ID of trademark to retrieve
        db: Session = Depends(get_db)  # Database session dependency
):
    """
    Retrieve a specific trademark by its unique ID.

    This endpoint fetches a single trademark record based on the provided ID.
    If the trademark doesn't exist, it returns a 404 error.
    """
    # Attempt to retrieve the trademark by ID
    db_trademark = crud_trademark.get_trademark(db, trademark_id=trademark_id)

    # If trademark doesn't exist, return 404 error
    if db_trademark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trademark with ID {trademark_id} not found"
        )

    return db_trademark


@router.put("/{trademark_id}", response_model=trademark_schemas.TrademarkResponse)
def update_trademark(
        trademark_id: int,  # Path parameter - ID of trademark to update
        trademark_update: trademark_schemas.TrademarkUpdate,  # Request body with update data
        db: Session = Depends(get_db)  # Database session dependency
):
    """
    Update an existing trademark by its ID.

    This endpoint allows partial updates - clients only need to provide
    the fields they want to change. Other fields remain unchanged.
    """
    # Attempt to update the trademark using CRUD function
    db_trademark = crud_trademark.update_trademark(db, trademark_id=trademark_id, trademark_update=trademark_update)

    # If trademark doesn't exist, return 404 error
    if db_trademark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trademark with ID {trademark_id} not found"
        )

    return db_trademark


@router.delete("/{trademark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trademark(
        trademark_id: int,  # Path parameter - ID of trademark to delete
        db: Session = Depends(get_db)  # Database session dependency
):
    """
    Delete a trademark by its ID.

    This endpoint permanently removes a trademark from the database.
    It returns HTTP 204 No Content on successful deletion.
    """
    # Attempt to delete the trademark using CRUD function
    success = crud_trademark.delete_trademark(db, trademark_id=trademark_id)

    # If trademark doesn't exist, return 404 error
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trademark with ID {trademark_id} not found"
        )

    # Return nothing (HTTP 204 No Content)
    # FastAPI automatically handles the empty response
    return


@router.get("/search/{name}", response_model=List[trademark_schemas.TrademarkResponse])
def search_trademarks(
        name: str,  # Path parameter - search term
        db: Session = Depends(get_db)  # Database session dependency
):
    """
    Search trademarks by name using partial, case-insensitive matching.

    This endpoint allows users to find trademarks by typing part of the name.
    The search is case-insensitive and matches any trademark containing the search term.
    """
    # Validate minimum search term length to prevent overly broad searches
    if len(name.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search term must have at least 2 characters"
        )

    # Perform the search using CRUD function
    # Strip whitespace to clean the search term
    trademarks = crud_trademark.search_trademarks_by_name(db, name=name.strip())
    return trademarks


@router.get("/filter/status/{status}", response_model=List[trademark_schemas.TrademarkResponse])
def filter_trademarks_by_status(
        status: str,  # Path parameter - status to filter by
        db: Session = Depends(get_db)  # Database session dependency
):
    """
    Filter trademarks by status using partial, case-insensitive matching.

    This endpoint allows filtering trademarks based on their status field.
    The filtering is case-insensitive and matches any status containing the term.
    """
    # Direct database query for simple filtering
    # Using ilike for case-insensitive partial matching
    trademarks = db.query(Trademark).filter(Trademark.status.ilike(f"%{status}%")).all()
    return trademarks