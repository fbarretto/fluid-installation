MAX_X = 200
MAX_Y = 200
MIN_FEEDRATE = 1
MAX_FEEDRATE = 10000

def interpolate_points_with_cubic_ease(norm_origin, norm_destination, max_accel=1.0, min_accel=0.001):
    distance = ((norm_destination[0] - norm_origin[0]) ** 2 + (norm_destination[1] - norm_origin[1]) ** 2) ** 0.5
    num_points = max(5, int(distance * 100))
    
    interpolated_points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        ease_factor = 3 * (t ** 2) - 2 * (t ** 3)
        x = norm_origin[0] + ease_factor * (norm_destination[0] - norm_origin[0])
        y = norm_origin[1] + ease_factor * (norm_destination[1] - norm_origin[1])
        
        accel_factor = min(6 * t * (1 - t), 1)
        accel_factor = min_accel + (max_accel - min_accel) * accel_factor
        
        if interpolated_points and interpolated_points[-1][2] == max_accel and accel_factor == max_accel:
            continue
        
        interpolated_points.append((x, y, accel_factor))
    
    return interpolated_points

def points_to_gcode(points):
    gcode = []
    for point in points:
        x, y, accel = point
        feedrate = MIN_FEEDRATE + (MAX_FEEDRATE - MIN_FEEDRATE) * accel
        gcode.append(f'G1 X{x * MAX_X:.2f} Y{y * MAX_Y:.2f} F{feedrate:.2f}')
    return "\n".join(gcode)

# Example usage:
origin = (0, 0)
destination = (150, 80)

origin = (origin[0] / MAX_X, origin[1] / MAX_Y)
destination = (destination[0] / MAX_X, destination[1] / MAX_Y)

interpolated_points = interpolate_points_with_cubic_ease(origin, destination)

for point in interpolated_points:
    x, y, accel = point
    print(f'Point: ({x}, {y}), Acceleration: {accel:.4f}')
gcode = points_to_gcode(interpolated_points)
print(gcode)
