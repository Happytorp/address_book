"""
Address Book FastAPI Application.

A RESTful API for managing addresses with geographical coordinates.
Provides CRUD operations and distance-based search functionality.

Features:
- Create, read, update, and delete addresses
- Search addresses within a specified distance from a point
- Geographical distance calculations using Haversine formula
- SQLite database for data persistence

Author: Address Book API Team
Version: 1.0.0
"""

import logging
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, engine, SessionLocal, AddressModel
from schemas import AddressOut, AddressCreate, AddressUpdate
from crud import create_address, get_address, update_address, delete_address, get_all_addresses
from utils import haversine_distance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Address Book API",
    description="A RESTful API for managing addresses with geographical coordinates",
    version="1.0.0",
    docs_url="/docs",
)


def get_db():
    """
    Dependency to get database session.

    Creates a new database session for each request and ensures
    proper cleanup after the request is completed.

    Yields:
        Session: SQLAlchemy database session

    Note:
        This function is used as a FastAPI dependency to provide
        database access to endpoint functions.
    """
    db = SessionLocal()
    try:
        logger.info("Database session created")
        yield db
    finally:
        logger.info("Database session closed")
        db.close()


@app.post("/addresses", response_model=AddressOut)
def create_addr(address: AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address record.

    Creates a new address entry in the database with the provided
    name and geographical coordinates.

    Args:
        address (AddressCreate): Address data including name, latitude, and longitude
        db (Session): Database session dependency

    Returns:
        AddressOut: The created address record with assigned ID

    Raises:
        HTTPException: 500 if database operation fails

    Example:
        POST /addresses/
        {
            "name": "Home",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    """
    logger.info(f"Creating new address: {address.name} at ({address.latitude}, {address.longitude})")

    try:
        db_address = create_address(db, address)
        logger.info(f"Successfully created address with ID: {db_address.id}")
        return db_address

    except Exception as e:
        logger.error(f"Failed to create address: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create address")


@app.get("/addresses", response_model=List[AddressOut])
def read_addrs(db: Session = Depends(get_db)):
    """
    Retrieve all address records.

    Fetches all address entries from the database.

    Args:
        db (Session): Database session dependency

    Returns:
        List[AddressOut]: List of all address records

    Raises:
        HTTPException: 500 if database operation fails

    Example:
        GET /addresses/
    """
    logger.info("Retrieving all addresses from database")

    try:
        addresses = get_all_addresses(db)
        logger.info(f"Successfully retrieved {len(addresses)} addresses")
        return addresses
    except Exception as e:
        logger.error(f"Failed to retrieve addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve addresses")


@app.get("/addresses/{address_id}", response_model=AddressOut)
def read_addr(address_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific address by ID.

    Fetches an address record from the database using its unique identifier.

    Args:
        address_id (int): Unique identifier of the address to retrieve
        db (Session): Database session dependency

    Returns:
        AddressOut: The requested address record

    Raises:
        HTTPException: 404 if address not found

    Example:
        GET /addresses/1
    """
    logger.info(f"Retrieving address with ID: {address_id}")

    try:
        db_address = get_address(db, address_id)
        logger.info(f"Successfully retrieved address: {db_address.name}")
        return db_address
    except Exception as e:
        logger.error(f"Address with ID {address_id} not found: {str(e)}")
        raise HTTPException(status_code=404, detail="Address not found")


@app.put("/addresses/{address_id}", response_model=AddressOut)
def update_addr(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    """
    Update an existing address record.

    Updates an address record with new data. All fields in the request
    will overwrite the existing values.

    Args:
        address_id (int): Unique identifier of the address to update
        address (AddressUpdate): New address data
        db (Session): Database session dependency

    Returns:
        AddressOut: The updated address record

    Raises:
        HTTPException: 404 if address not found, 500 if update fails

    Example:
        PUT /addresses/1
        {
            "name": "Work",
            "latitude": 40.7589,
            "longitude": -73.9851
        }
    """
    logger.info(f"Updating address with ID: {address_id}")
    try:
        db_address = update_address(db, address_id, address)
        logger.info(f"Successfully updated address {address_id} to: {db_address.name}")
        return db_address
    except Exception as e:
        logger.error(f"Failed to update address {address_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update address")


@app.delete("/addresses/{address_id}")
def delete_addr(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address record.

    Permanently removes an address record from the database.

    Args:
        address_id (int): Unique identifier of the address to delete
        db (Session): Database session dependency

    Returns:
        dict: Success message confirming deletion

    Raises:
        HTTPException: 404 if address not found, 500 if deletion fails

    Example:
        DELETE /addresses/1
    """
    logger.info(f"Deleting address with ID: {address_id}")

    try:
        delete_address(db, address_id)
        logger.info(f"Successfully deleted address with ID: {address_id}")
        return {"detail": "Address deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete address {address_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete address")


@app.get("/addresses_within_distance", response_model=List[AddressOut])
def get_addresses_within_distance(
        lat: float,
        lon: float,
        distance_km: float,
        db: Session = Depends(get_db)
):
    """
    Find addresses within a specified distance from a point.

    Searches for all addresses within a given radius from a specified
    geographical point using the Haversine distance formula.

    Args:
        lat (float): Latitude of the search center (-90 to 90)
        lon (float): Longitude of the search center (-180 to 180)
        distance_km (float): Search radius in kilometers (must be positive)
        db (Session): Database session dependency

    Returns:
        List[AddressOut]: List of addresses within the specified distance

    Note:
        The search uses great circle distance calculations, which may
        not account for actual travel distances or geographical obstacles.

    Example:
        GET /addresses/?lat=40.7128&lon=-74.0060&distance_km=10
    """
    logger.info(f"Searching for addresses within {distance_km}km of ({lat}, {lon})")

    try:
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")

        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")

        if distance_km <= 0:
            raise ValueError("Distance must be a positive value")

        # Get all addresses from database
        all_addresses = db.query(AddressModel).all()
        logger.info(f"Retrieved {len(all_addresses)} addresses from database")

        result = []

        # Calculate distance for each address and filter
        for addr in all_addresses:
            try:
                dist = haversine_distance(lat, lon, addr.latitude, addr.longitude)
                logger.info(f"Distance to {addr.name} (ID: {addr.id}): {dist:.2f}km")

                if dist <= distance_km:
                    result.append(addr)

            except Exception as e:
                logger.warning(f"Failed to calculate distance for address {addr.id}: {str(e)}")
                continue

        logger.info(f"Found {len(result)} addresses within {distance_km}km radius")
        return result

    except Exception as e:
        logger.error(f"Failed to search addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search addresses")


@app.get("/health_check")
def health_check():
    """
    Health check endpoint.

    Simple endpoint to verify that the API is running and responsive.
    Used for monitoring and load balancer health checks.

    Returns:
        dict: Status message indicating API health

    Example:
        GET /health_check
    """
    logger.info("Health check requested")
    return {"status": "Address Book API is running", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Address Book API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000
    )
