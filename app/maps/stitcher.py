import os
import pickle


def get_help():
    """Get help"""
    for func in cmd_map.values():
        help(func)

def clear_quilt():
    """Empty the quilt"""
    global quilt
    resp = None
    has_responded_once = False
    while not (resp in ["y", "n"]):
        if has_responded_once:
            print("Invalid response.")
        resp = input("Are you sure you want to clear the quilt [y/n]?: ")
        has_responded_once = True
    if resp == "y":
        quilt = []
        print("Cleared.")
    else:
        print("Cancelling action.")

def add():
    """Add a file to the quilt"""
    done = False
    while not done:
        f_name = input("Which file would you like to add [ENTER to exit]?: ")
        if os.path.exists(f_name):
            quilt.append(f_name)
        elif f_name != "":
            print("Path does not exist.")
            done = True
        else:
            done = True

def stitch():
    """Connect two pieces of the quilt"""
    ends = input("Which would you like to stitch (separate with hyphen)?: ")
    ends = ends.split("-")
    if len(ends) != 2:
        print("Invalid stitch.")
        return
    try:
        connection = (int(ends[0]), int(ends[1]))
        connections.append(connection)
    except ValueError:
        print("Invalid stitch. Please enter indices.")

def print_quilt():
    """Display the quilt"""
    for i, section in enumerate(quilt):
        print(i + 1, section)

def finish():
    """Finish and save the quilt"""
    pass

def _quit():
    "Leave the program without saving"
    global running
    running = False

quilt = []
connections = []
cmd_map = {
    "help": get_help,
    "clear": clear_quilt,
    "add": add,
    "quilt": print_quilt,
    "finish": finish,
    "quit": _quit
}

running = True
while running:
    cmd = input("Enter a command (type help): ")
    if cmd in cmd_map:
        cmd_map[cmd]()
    else:
        print("Invalid command")
    print("\n")