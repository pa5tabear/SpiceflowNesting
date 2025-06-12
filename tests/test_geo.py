import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.geo import haversine_miles


def test_haversine():
    # Distance from Liberty & Main to itself should be ~0
    assert haversine_miles(42.2808, -83.7480) < 0.01
