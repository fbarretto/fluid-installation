from interpolation import Interpolator
from dsf.connections import CommandConnection
import random, time

MAX_X = 290
MAX_Y = 215 # Technically the Y-Max is 250, but the magnet will collide with the extrusion if it goes beyond 215
MIN_FEEDRATE = 1000 # this is arbitrary
MAX_FEEDRATE = 10608 # Max Possible Feedrate (Max Speed is 176.8 mm/sec)
NUM_POINTS_FACTOR = 100 # Number of points per unit of normalized distance: higher values means more points.

def main():
    current_position = (0, 0)

    while True:
        origin = current_position
        destination = (random.randrange(0, MAX_X), random.randrange(0, MAX_Y))
        
        # Create an interpolator object
        interpolator = Interpolator(max_x=MAX_X, max_y=MAX_Y, min_feedrate=MIN_FEEDRATE, max_feedrate=MAX_FEEDRATE, num_points_factor=NUM_POINTS_FACTOR)
        
        #normalize points
        norm_origin, norm_destination = normalize_points(origin, destination)
        
        #interpolate points, set skip_duplicate_acc to True to skip points with the same acceleration
        points = interpolator.interpolate_points_with_cubic_ease(norm_origin, norm_destination, skip_duplicate_acc=True)

        #convert points to gcode
        for point in points:
            GCode = interpolator.point_to_gcode(point)
            # print(GCode)
            send_GCode(GCode)
        
        current_position = destination
        time.sleep(2)

def normalize_points(origin, destination):
    norm_origin = (origin[0] / MAX_X, origin[1] / MAX_Y)
    norm_destination = (destination[0] / MAX_X, destination[1] / MAX_Y)
    return norm_origin, norm_destination

def send_GCode(GCode):
    command_connection = CommandConnection(debug=True)
    command_connection.connect()

    try:
        # Perform a simple command and wait for its output
        res = command_connection.perform_simple_code(GCode, async_exec = True)
        print(res)
    finally:
        command_connection.close()


if __name__ == "__main__":
    main()