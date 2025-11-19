"""
This module contains all the helper functions used across the Address Book API.
"""

import logging
import math
from decorators import log_input_output

# Configure logging
logger = logging.getLogger(__name__)


@log_input_output()
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.

    Uses the Haversine formula to calculate the shortest distance between
    two points on the Earth's surface given their latitude and longitude
    coordinates in decimal degrees.

    Args:
        lat1 (float): Latitude of the first point in decimal degrees
        lon1 (float): Longitude of the first point in decimal degrees
        lat2 (float): Latitude of the second point in decimal degrees
        lon2 (float): Longitude of the second point in decimal degrees

    Returns:
        float: Distance between the two points in kilometers
    """
    logger.info(f"Calculating distance between ({lat1}, {lon1}) and ({lat2}, {lon2})")

    EARTH_RADIUS_KM = 6371

    if not (-90 <= lat1 <= 90) or not (-90 <= lat2 <= 90):
        logger.error(f"Invalid latitude values: lat1={lat1}, lat2={lat2}")
        raise ValueError("Latitude values must be between -90 and 90 degrees")

    if not (-180 <= lon1 <= 180) or not (-180 <= lon2 <= 180):
        logger.error(f"Invalid longitude values: lon1={lon1}, lon2={lon2}")
        raise ValueError("Longitude values must be between -180 and 180 degrees")

    # Convert latitude and longitude from degrees to radians
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(delta_lon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS_KM * c

    logger.info(f"Calculated distance: {distance:.2f} km")
    return distance
