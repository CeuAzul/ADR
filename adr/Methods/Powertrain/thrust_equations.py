def get_axial_thrust_from_linear_model(air_density, velocity, static_thrust, linear_coefficient):
    cond1 = air_density > 0
    cond2 = velocity >= 0

    if cond1 and cond2:
        air_density_factor = air_density/1.225
        return (static_thrust + linear_coefficient * velocity) * air_density_factor
    else:
        raise ValueError(
            f'Air density must be positive. \
              Velocity must be equal or greater than zero. \
              Found density={air_density} and velocity = {velocity}.')
