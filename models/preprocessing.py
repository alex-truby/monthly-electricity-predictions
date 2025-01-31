def transform_occupants(occupants: str) -> int:
    return int(occupants.replace('+', ''))

def transform_vintage(vintage: str) -> int:
    vintage = vintage.replace('s', '')
    vintage = vintage.replace('<', '')
    return int(vintage)

def transform_string_to_int(input_var: str) -> int:
    return int(input_var)

def transform_set_point(setpoint: str) -> float:
    return float(setpoint.replace('F', ''))

def calculate_temperature_deviation(average_temperature: float, heating_setpoint: float, cooling_setpoint: float) -> float:
    """Calculate the temperature deviation based on the provided logic."""
    if average_temperature > cooling_setpoint:
        return float(average_temperature - cooling_setpoint)
    elif average_temperature < heating_setpoint:
        return float(average_temperature - heating_setpoint)
    else:
        return 0.0