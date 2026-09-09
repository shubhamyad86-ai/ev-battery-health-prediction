import pytest

from src.validator import validate_battery_input


VALID_BATTERY = {
    "battery_voltage": 400,
    "battery_temp": 28,
    "soc": 80,
    "soh": 92,
    "charge_cycles": 900,
    "internal_resistance": 0.04,
    "battery_current": 35,
    "battery_age_days": 4 * 365,  # 4 years, expressed in days
}


def test_valid_battery_passes():
    assert validate_battery_input(VALID_BATTERY) is True


def test_invalid_voltage_raises():
    battery = {**VALID_BATTERY, "battery_voltage": 900}
    with pytest.raises(ValueError):
        validate_battery_input(battery)


def test_invalid_temperature_raises():
    battery = {**VALID_BATTERY, "battery_temp": 150}
    with pytest.raises(ValueError):
        validate_battery_input(battery)


def test_invalid_soc_raises():
    battery = {**VALID_BATTERY, "soc": 150}
    with pytest.raises(ValueError):
        validate_battery_input(battery)


def test_negative_internal_resistance_raises():
    battery = {**VALID_BATTERY, "internal_resistance": -0.01}
    with pytest.raises(ValueError):
        validate_battery_input(battery)


def test_battery_age_out_of_range_raises():
    battery = {**VALID_BATTERY, "battery_age_days": 30 * 365}  # 30 years
    with pytest.raises(ValueError):
        validate_battery_input(battery)
