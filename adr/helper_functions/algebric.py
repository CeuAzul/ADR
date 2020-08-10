import math
import vec


def rotate(vector2d, angle_radians):
    x, y = vector2d.x, vector2d.y
    xx = x * math.cos(angle_radians) - y * math.sin(angle_radians)
    yy = x * math.sin(angle_radians) + y * math.cos(angle_radians)
    return vec.Vector2(xx, yy)


def translate(vector2d, displacement_x, displacement_y):
    displacement_vector = vec.Vector2(displacement_x, displacement_y)
    return vector2d + displacement_vector


def transform(vector2d, angle_radians, displacement_x, displacement_y):
    rotated_vector = rotate(vector2d, angle_radians)
    displaced_vector = translate(
        rotated_vector, displacement_x, displacement_y)
    return displaced_vector


def component_vector_in_absolute_frame(vector, component):
    return transform(vector, component.angle, *component.position)


def component_vector_coords_in_absolute_frame(vector_origin, vector, component):
    absolute_origin = component_vector_in_absolute_frame(
        vector_origin, component)
    absolute_end = component_vector_in_absolute_frame(
        vector_origin+vector, component)
    return (*absolute_origin, *absolute_end)
