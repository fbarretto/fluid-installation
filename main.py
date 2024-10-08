from interpolation import Interpolator
# from dsf.connections import CommandConnection
import random, time
from pythonosc import dispatcher, osc_server

MAX_X = 290
MAX_Y = 215 # Technically the Y-Max is 250, but the magnet will collide with the extrusion if it goes beyond 215
MIN_FEEDRATE = 1000 # this is arbitrary
MAX_FEEDRATE = 10608 # Max Possible Feedrate (Max Speed is 176.8 mm/sec)
NUM_POINTS_FACTOR = 100 # Number of points per unit of normalized distance: higher values means more points.

DEBUG = False
current_position = (0, 0)

def main():
    while True:
        if (DEBUG):
            destination = (random.randrange(0, MAX_X), random.randrange(0, MAX_Y))
            norm_destination = normalize_point(destination)
            move_to(norm_destination, True)
            distance = ((destination[0] - current_position[0]) ** 2 + (destination[1] - current_position[1]) ** 2) ** 0.5
            time.sleep(distance/MAX_FEEDRATE * 10) # wait until the movement is complete, then generate the next point to move to (THIS IS AN APPROXIMATION)

def move_to(destination):
    global current_position
    interpolator = Interpolator(max_x=MAX_X, max_y=MAX_Y, min_feedrate=MIN_FEEDRATE, max_feedrate=MAX_FEEDRATE, num_points_factor=NUM_POINTS_FACTOR)
    # norm_origin, norm_destination = normalize_points(origin, destination)
    points = interpolator.interpolate_points_with_cubic_ease(current_position, destination, skip_duplicate_acc=True)
    gcode_commands = points_to_gcode(points)
    print(f"Moving from {current_position} to {destination}")
    print(gcode_commands)
    # send_GCode(gcode_commands, async_exec=False)
    current_position = destination

def points_to_gcode(points):
    interpolator = Interpolator(max_x=MAX_X, max_y=MAX_Y, min_feedrate=MIN_FEEDRATE, max_feedrate=MAX_FEEDRATE, num_points_factor=NUM_POINTS_FACTOR)
    gcode_commands = []
    for point in points:
        GCode = interpolator.point_to_gcode(point)
        gcode_commands.append(GCode)
    return "\n".join(gcode_commands)
    
def normalize_points(origin, destination):
    norm_origin = (origin[0] / MAX_X, origin[1] / MAX_Y)
    norm_destination = (destination[0] / MAX_X, destination[1] / MAX_Y)
    return norm_origin, norm_destination

def normalize_point(point):
    return (point[0] / MAX_X, point[1] / MAX_Y)

def send_GCode(GCode, async_exec = False):
    command_connection = CommandConnection(debug=True)
    command_connection.connect()

    try:
        # Perform a simple command and wait for its output
        res = command_connection.perform_simple_code(GCode, async_exec = async_exec)
        #print(res)
    finally:
        command_connection.close()

def osc_move_handler(unused_addr, x, y): 
    go_to = (x, y)
    if (DEBUG):
        print(f"Received new position: {go_to}")
    move_to(go_to)

def start_osc_server():
    disp = dispatcher.Dispatcher()
    if (not DEBUG):
        disp.map("/pos1", osc_move_handler)
    # disp.map("/x", lambda unused_addr, x: update_position(x, None))
    # disp.map("/y", lambda unused_addr, y: update_position(None, y))
    # disp.set_default_handler(lambda addr, *args: print(f"Received message: {addr}, with arguments: {args}"))

    server = osc_server.ThreadingOSCUDPServer(("localhost", 5005), disp)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

if __name__ == "__main__":
    import threading
    osc_thread = threading.Thread(target=start_osc_server)
    osc_thread.daemon = True
    osc_thread.start()
    main()