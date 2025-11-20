import pytest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from address_book.utils import haversine_distance

def test_haversine_same_point():
    """Distance between the same coordinates should be 0."""
    dist = haversine_distance(12.9716, 77.5946, 12.9716, 77.5946)
    assert dist == pytest.approx(0.0, abs=0.0001)


def test_haversine_valid_distance():
    """
    Validate distance between Bangalore and Mysore.
    Actual ≈ 128 km (approx).
    """
    dist = haversine_distance(12.9716, 77.5946, 12.2958, 76.6394)
    assert dist == pytest.approx(128, rel=0.1)   # allow 10% tolerance


def test_invalid_latitude():
    """Latitude outside [-90, 90] should raise ValueError."""
    with pytest.raises(ValueError):
        haversine_distance(100, 77.5, 12.9, 77.5)


def test_invalid_longitude():
    """Longitude outside [-180, 180] should raise ValueError."""
    with pytest.raises(ValueError):
        haversine_distance(12.9, 500, 12.9, 77.5)

