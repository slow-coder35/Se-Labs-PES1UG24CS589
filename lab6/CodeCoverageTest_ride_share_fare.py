"""Stage 1: exercise every executable line of the unchanged application."""

import pytest

from ride_share_fare import extra_distance_fare, pickup_status, seats_and_bags_ok


def test_unknown_cab():
    with pytest.raises(ValueError, match="^unknown cab type$"):
        extra_distance_fare("van", 10, "city", False)


def test_negative_distance():
    with pytest.raises(ValueError, match="^invalid distance$"):
        extra_distance_fare("mini", -1, "city", False)


@pytest.mark.parametrize("cab,distance,zone,subscriber,expected", [
    ("sedan", 5, "city", False, 0),
    ("mini", 9, "city", True, 12),
    ("suv", 33, "outstation", False, 630),
])
def test_fare(cab, distance, zone, subscriber, expected):
    assert extra_distance_fare(cab, distance, zone, subscriber) == expected


@pytest.mark.parametrize("passengers,bags,wheelchair,expected", [
    (2, 1, False, True),
    (5, 0, False, False),
    (2, 3, True, True),
])
def test_capacity(passengers, bags, wheelchair, expected):
    assert seats_and_bags_ok(passengers, bags, wheelchair) is expected


@pytest.mark.parametrize("minutes,scheduled,airport,expected", [
    (20, True, True, "on_time"),
    (0, False, False, "delayed"),
    (-11, False, False, "missed"),
])
def test_pickup(minutes, scheduled, airport, expected):
    assert pickup_status(minutes, scheduled, airport) == expected
