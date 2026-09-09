try:
    from .battery_predictor import BatteryPredictor
    from .validator import validate_battery_input
except ImportError:
    from battery_predictor import BatteryPredictor
    from validator import validate_battery_input


def get_user_input():

    print("\nEnter Battery Information\n")

    battery = {}

    battery["battery_voltage"] = float(input("Battery Voltage (V): "))
    battery["battery_current"] = float(input("Battery Current (A): "))
    battery["soc"] = float(input("State of Charge (%): "))
    battery["battery_temp"] = float(input("Battery Temperature (°C): "))
    battery["ambient_temp"] = float(input("Ambient Temperature (°C): "))
    battery["charge_cycles"] = int(input("Charge Cycles: "))
    battery["fast_charge_count"] = int(input("Fast Charge Count: "))
    battery["total_distance_km"] = float(input("Total Distance (km): "))
    battery["trip_distance_km"] = float(input("Trip Distance (km): "))
    battery["avg_speed_kmh"] = float(input("Average Speed (km/h): "))
    battery["max_speed_kmh"] = float(input("Maximum Speed (km/h): "))
    battery["acceleration_ms2"] = float(input("Acceleration (m/s²): "))
    battery["regenerative_energy_kwh"] = float(input("Regenerative Energy (kWh): "))
    battery["energy_consumption_kwh_100km"] = float(input("Energy Consumption (kWh/100km): "))
    battery["motor_temp"] = float(input("Motor Temperature (°C): "))
    battery["inverter_temp"] = float(input("Inverter Temperature (°C): "))
    battery["charging_duration_min"] = float(input("Charging Duration (min): "))
    battery["cell_voltage_std"] = float(input("Cell Voltage Std: "))
    battery["internal_resistance"] = float(input("Internal Resistance (Ohm): "))
    battery["battery_age_days"] = int(input("Battery Age (Days): "))
    battery["humidity"] = float(input("Humidity (%): "))
    battery["remaining_range_km"] = float(input("Remaining Range (km): "))
    battery["rul_cycles"] = int(input("Remaining Useful Life (Cycles): "))
    # Placeholder only: SOH is the value we're predicting, not a real
    # input. It's set to a valid value purely so validate_soh() passes;
    # it is never included in the feature vector sent to the model.
    battery["soh"] = 100.0

    # -----------------------------
    # Engineered Features
    # -----------------------------

    battery["battery_power_kw"] = (
        battery["battery_voltage"] * battery["battery_current"]
    ) / 1000

    battery["battery_age_years"] = battery["battery_age_days"] / 365

    battery["fast_charge_ratio"] = (
        battery["fast_charge_count"] /
        (battery["charge_cycles"] + 1)
    )

    battery["battery_stress_index"] = (
        battery["battery_temp"] *
        battery["internal_resistance"]
    )

    battery["temperature_difference"] = (
        battery["battery_temp"] -
        battery["ambient_temp"]
    )

    battery["avg_distance_per_cycle"] = (
        battery["total_distance_km"] /
        (battery["charge_cycles"] + 1)
    )

    battery["power_to_voltage_ratio"] = (
        battery["battery_power_kw"] /
        battery["battery_voltage"]
        if battery["battery_voltage"] != 0 else 0
    )

    battery["range_per_soc"] = (
        battery["remaining_range_km"] /
        (battery["soc"] + 1)
    )

    return battery


def main():

    print("=" * 60)
    print("EV BATTERY HEALTH PREDICTION SYSTEM")
    print("=" * 60)

    battery = get_user_input()

    validate_battery_input(battery)

    predictor = BatteryPredictor()

    features = [battery[name] for name in predictor.feature_names]

    prediction = predictor.predict(features)

    print("\n")
    print("=" * 60)
    print("BATTERY HEALTH PREDICTION")
    print("=" * 60)

    print(f"Predicted SOH : {prediction:.2f}%")

    if prediction >= 90:
        status = "Excellent"
    elif prediction >= 80:
        status = "Good"
    elif prediction >= 70:
        status = "Moderate"
    elif prediction >= 60:
        status = "Weak"
    else:
        status = "Replace Battery"

    print(f"Battery Status : {status}")


if __name__ == "__main__":
    main()
