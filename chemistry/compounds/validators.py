def gps_coordinates_validator(value):
    return value[0] >= 0 and value[0] <= 90 and value[1] >= 0 and value[1] <= 180
