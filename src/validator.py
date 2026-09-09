"""
=========================================
Battery Input Validator
=========================================
"""

def validate_voltage(voltage):
    if not 250 <= voltage <= 450:
        raise ValueError(
            f"Voltage {voltage}V is outside the valid range (250-450V)."
        )


def validate_temperature(temp):
    if not -20 <= temp <= 80:
        raise ValueError(
            f"Temperature {temp}°C is outside the valid range (-20 to 80°C)."
        )


def validate_soc(soc):
    if not 0 <= soc <= 100:
        raise ValueError(
            f"SOC {soc}% must be between 0 and 100."
        )


def validate_soh(soh):
    if not 0 <= soh <= 100:
        raise ValueError(
            f"SOH {soh}% must be between 0 and 100."
        )


def validate_charge_cycles(cycles):
    if not 0 <= cycles <= 5000:
        raise ValueError(
            f"Charge Cycles {cycles} must be between 0 and 5000."
        )


def validate_internal_resistance(resistance):
    if resistance < 0:
        raise ValueError(
            "Internal Resistance cannot be negative."
        )


def validate_current(current):
    if not -500 <= current <= 500:
        raise ValueError(
            "Current is outside the supported range."
        )


def validate_battery_age(age):
    if not 0 <= age <= 25:
        raise ValueError(
            "Battery age must be between 0 and 25 years."
        )
    
    
def validate_battery_input(data):
    """
    Validate all battery input values.
    """

    validate_voltage(data["battery_voltage"])
    validate_temperature(data["battery_temp"])
    validate_soc(data["soc"])
    validate_soh(data["soh"])
    validate_charge_cycles(data["charge_cycles"])
    validate_internal_resistance(data["internal_resistance"])
    validate_current(data["battery_current"])
    validate_battery_age(data["battery_age_days"] / 365)  # Convert days to years for validation

    return True