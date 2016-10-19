import os

LEVEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'levels')
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data')


def get_levels():
    """Function for reading the levels folder"""
    files = os.listdir(LEVEL_PATH)
    levels = []
    for f in files:
        if f.endswith(".lvl"):
            levels.append(int(f.replace('.lvl', '')))
    return sorted(levels)


def get_level_path(level_nr):
    return os.path.join(LEVEL_PATH, str(level_nr).zfill(4)+'.lvl')


def get_lock_status():
    """Get the lock status for the levels"""
    levels = {}
    try:
        f = open(os.path.join(DATA_PATH, 'levels.txt'), 'r')
    except IOError:
        # The file doesn't exist
        _generate_levels_file()
        f = open(os.path.join(DATA_PATH, 'levels.txt'), 'r')
    for line in f:
        fields = line.strip().split()
        levels[fields[0]] = fields[1]
    file_levels = get_levels()
    if file_levels != sorted([int(i) for i in levels.keys()]):
        # The levels in the level folder have changed
        _update_levels_file(file_levels, levels)
        f = open(os.path.join(DATA_PATH, 'levels.txt'), 'r')
        for line in f:
            fields = line.strip().split()
            levels[fields[0]] = fields[1]
    return levels


def update_lock_status_on_level(level):
    """Update the lock status on a level"""
    levels = get_lock_status()
    levels[str(level)] = '1'
    _update_levels_file(get_levels(), levels)


def _update_levels_file(file_levels, levels):
    """Internal function for updating the data in the levels file."""
    lvl = open(os.path.join(DATA_PATH, 'levels.txt'), 'w')
    reset_rest = False
    for f in file_levels:
        if str(f) in levels and not reset_rest:
            lvl.write(str(f) + " " + str(levels[str(f)]) + "\n")
        else:
            reset_rest = True
            lvl.write(str(f) + " " + str(0) + "\n")


def _generate_levels_file():
    """Generate the levels file"""
    lvl = open(os.path.join(DATA_PATH, 'levels.txt'), 'w')
    files = os.listdir(LEVEL_PATH)
    for f in files:
        if f.endswith(".lvl"):
            lvl.write(str(int(f.replace('.lvl', ''))) + " " + str(0) + "\n")
