"""Stage 2: independently cover decisions and fare/capacity/pickup boundaries."""

import pytest

from ride_share_fare import extra_distance_fare, pickup_status, seats_and_bags_ok


@pytest.mark.parametrize("cab,distance,message", [
    ("van", 10, "unknown cab type"),
    ("mini", -0.1, "invalid distance"),
])
def test_invalid_fare_inputs(cab, distance, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        extra_distance_fare(cab, distance, "city", False)


@pytest.mark.parametrize("cab,distance,zone,subscriber,expected", [
    ("mini", 0, "city", False, 0),
    ("mini", 5, "city", False, 0),
    ("mini", 5.5, "city", False, 6),
    ("sedan", 8, "city", False, 0),
    ("sedan", 9, "city", False, 12),
    ("suv", 12, "city", False, 0),
    ("suv", 13, "city", False, 12),
    ("mini", 8, "city", True, 0),
    ("mini", 9, "city", True, 12),
    ("sedan", 11, "city", True, 0),
    ("sedan", 12, "city", True, 12),
    # SUV subscribers receive no additional included kilometres.
    ("suv", 13, "city", True, 12),
    ("mini", 6, "outstation", False, 18),
    ("mini", 25, "city", False, 240),
    ("mini", 26, "city", False, 420),
    ("mini", 25, "outstation", False, 360),
    ("mini", 26, "outstation", False, 630),
    # Current implementation treats other zone strings as non-city.
    ("mini", 6, "other", False, 18),
    ("mini", 26, "other", False, 546),
])
def test_fare_boundaries(cab, distance, zone, subscriber, expected):
    assert extra_distance_fare(cab, distance, zone, subscriber) == expected


@pytest.mark.parametrize("passengers,bags,wheelchair,expected", [
    (0, 0, False, True),
    (4, 2, False, True),
    (5, 0, False, False),
    (4, 3, False, False),
    (2, 2, True, True),
    (3, 0, True, False),
    # The wheelchair branch uses passenger count only, including many bags.
    (2, 10, True, True),
])
def test_capacity_boundaries(passengers, bags, wheelchair, expected):
    assert seats_and_bags_ok(passengers, bags, wheelchair) is expected


@pytest.mark.parametrize("scheduled,airport,cutoff", [
    (False, False, 5),
    (True, False, 10),
    (False, True, 15),
    (True, True, 20),
])
@pytest.mark.parametrize("offset,expected", [
    (1, "on_time"),
    (0, "on_time"),
    (-1, "delayed"),
    (-14, "delayed"),
    (-15, "delayed"),
    (-16, "missed"),
])
def test_pickup_boundaries(scheduled, airport, cutoff, offset, expected):
    assert pickup_status(cutoff + offset, scheduled, airport) == expected
