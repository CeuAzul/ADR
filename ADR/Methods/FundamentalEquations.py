def lift(air_density, velocity, area, lift_coefficient):
    lift = 0.5 * air_density * velocity ** 2 * area * lift_coefficient
    return lift


def drag(air_density, velocity, area, drag_coefficient):
    drag = 0.5 * air_density * velocity ** 2 * area * drag_coefficient
    return drag


def moment(air_density, velocity, area, moment_coefficient):
    moment = 0.5 * air_density * velocity ** 2 * area * moment_coefficient
    return moment
