"""
This module defines the data models used for request/response validation
and serialization in the FastAPI application.
"""

import logging
from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class Addressbase(BaseModel):
    """
    Base address schema with common fields.

    This base class contains the common fields shared across
    all address-related schemas including validation constraints.

    Attributes:
        name (str): Address name/description (max 10 characters)
        latitude (float): Latitude coordinate (between -90 and 90)
        longitude (float): Longitude coordinate (between -180 and 180)
    """
    name: str = Field(..., max_length=10)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class AddressCreate(Addressbase):
    """
    Schema for creating a new address.

    Inherits all fields from Addressbase and is used when
    creating a new address record via POST requests.
    """
    pass


class AddressUpdate(Addressbase):
    """
    Schema for updating an existing address.

    Inherits all fields from Addressbase and is used when
    updating an existing address record via PUT requests.
    """
    pass


class AddressOut(Addressbase):
    """
    Schema for address output/response.

    Extends Addressbase with the database ID field for
    returning address data in API responses.

    Attributes:
        id (int): Unique identifier from the database
    """
    id: int = Field(...)

    class Config:
        """
        Enables automatic conversion from SQLAlchemy ORM objects
        to Pydantic models for JSON serialization.
        """
        from_attributes = True

