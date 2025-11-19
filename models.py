"""
Database models and configuration for the Address Book API.

This module contains the SQLAlchemy models and database configuration
for storing address information with geographical coordinates.
"""

import logging
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configure logging
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///address_book.db"
Base = declarative_base()

# Create database engine
logger.info(f"Creating database engine with URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class AddressModel(Base):
    """
    Address model representing a geographical location.

    This model stores address information including name and geographical
    coordinates (latitude and longitude) in the database.

    Attributes:
        id (int): Primary key identifier for the address
        name (str): Human-readable name/description of the address
        latitude (float): Latitude coordinate (-90 to 90 degrees)
        longitude (float): Longitude coordinate (-180 to 180 degrees)
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
