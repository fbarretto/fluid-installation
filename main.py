from interpolation import Interpolator
# from dsf.connections import CommandConnection

MAX_X = 200
MAX_Y = 200
MIN_FEEDRATE = 1
MAX_FEEDRATE = 10000

def main():
    origin = (0, 0)
    destination = (150, 80)
    
    # Create an interpolator object
    interpolator = Interpolator(max_x=MAX_X, max_y=MAX_Y, min_feedrate=MIN_FEEDRATE, max_feedrate=MAX_FEEDRATE)
    
    #normalize points
    norm_origin, norm_destination = normalize_points(origin, destination)
    
    #interpolate points
    points = interpolator.interpolate_points_with_cubic_ease(norm_origin, norm_destination)
    
    #convert points to gcode
    for point in points:
        GCode = interpolator.point_to_gcode(point)
        print(GCode)
        #send_simple_code(GCode)


def normalize_points(origin, destination):
    norm_origin = (origin[0] / MAX_X, origin[1] / MAX_Y)
    norm_destination = (destination[0] / MAX_X, destination[1] / MAX_Y)
    return norm_origin, norm_destination

def send_GCode(GCode):
    command_connection = CommandConnection(debug=True)
    command_connection.connect()

    try:
        # Perform a simple command and wait for its output
        res = command_connection.perform_simple_code("Gcode")
        print(res)
    finally:
        command_connection.close()


if __name__ == "__main__":
    main()