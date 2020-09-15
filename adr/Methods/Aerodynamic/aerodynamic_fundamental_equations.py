def get_lift(air_density, velocity, area, lift_coefficient):
    cond1 = air_density > 0
    cond2 = area > 0
    cond3 = velocity >= 0

    if cond1 and cond2 and cond3:
        return 0.5 * air_density * velocity ** 2 * area * lift_coefficient
    else:
        raise ValueError(
            f'Air density and area must be positive. \
              Velocity must be equal or greater than zero. \
              Found density={air_density}, area={area} and velocity = {velocity}.')


def get_drag(air_density, velocity, area, drag_coefficient):
    cond1 = air_density > 0
    cond2 = area > 0
    cond3 = velocity >= 0
    cond4 = drag_coefficient >= 0

    if cond1 and cond2 and cond3 and cond4:
        return 0.5 * air_density * velocity ** 2 * area * drag_coefficient
    else:
        raise ValueError(
            f'Air density and area must be positive. \
              Velocity and drag coefficient must be equal or greater than zero. \
              Found density={air_density}, area={area}, velocity = {velocity} and CD = {drag_coefficient}.')


def get_moment(air_density, velocity, area, moment_coefficient, chord):
    cond1 = air_density > 0
    cond2 = area > 0
    cond3 = velocity >= 0
    cond4 = chord > 0

    if cond1 and cond2 and cond3 and cond4:
        return 0.5 * air_density * velocity ** 2 * area * moment_coefficient * chord
    else:
        raise ValueError(
            f'Air density, area and chord must be positive. \
              Velocity must be equal or greater than zero. \
              Found density={air_density}, area={area}, velocity = {velocity} and chord = {chord}.')
