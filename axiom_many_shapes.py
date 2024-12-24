#!/usr/bin/env python3
import curses
import logging
import math
import plotly.graph_objects as go
import sys
import random

LOG_FILENAME = "layer_axiom_game.log"
OUTPUT_FILENAME = "matrix_visualization.html"

logging.basicConfig(
    filename=LOG_FILENAME,
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

DEFAULT_CHAR = "◦"  # \u25E6
CENTER_CHAR = "O"

# Visualization config:
LAYER_VISUALIZATION_MODES = {
    "layer_0": "markers",
    "layer_1": "lines+markers",
    "layer_1_plus": "lines",
}

AXIOM_CONFIGS = {
    'A': {'color': 'red',    'label': 'A (XY plane)',           'opacity': 1},
    'B': {'color': 'blue',   'label': 'B (YZ plane)',           'opacity': 1},
    'C': {'color': 'green',  'label': 'C (XZ plane)',           'opacity': 1},
    'D': {'color': 'purple', 'label': 'D (Diagonal plane Y1)',  'opacity': 1},
    'E': {'color': 'brown',  'label': 'E (Diagonal plane Y2)',  'opacity': 1},
    'F': {'color': 'black',  'label': 'F (Diagonal plane Y3)',  'opacity': 1},
    'H': {'color': 'purple', 'label': 'H (Diagonal plane -Y1)', 'opacity': 1},
    'I': {'color': 'brown',  'label': 'I (Diagonal plane -Y2)', 'opacity': 1},
    'J': {'color': 'black',  'label': 'J (Diagonal plane -Y3)', 'opacity': 1},
}

LAYER0_OPACITY = 1
LAYER1_OPACITY = 1

# These can be overridden via CLI:
PREFILL = False
FILL_MODE = "full"  # "full", "partial", or "random"
SHAPE = "circle"    # "circle", "square", "polygon:N"

# Holds each layer’s data; keys: (layer, axiom) => (grid, read_only)
data = {}

# Current “game state” for curses
current_layer = 0
current_axiom = 'A'
cursor_x, cursor_y = 0, 0

# Example default fill patterns (each is a list of strings):
FILLS = {
    'A': ['B'],
    'B': ['B'],
    'C': ['C'],
    'D': ['D'],
    'E': ['E'],
    'F': ['F'],
    'H': ['H'],
    'I': ['I'],
    'J': ['J'],
}

# ---------------------------------------------------------------------
# 1) LAYER / GRID CREATION
# ---------------------------------------------------------------------
def layer_dimension(layer):
    return 2 * layer + 1

def create_layer_axiom(layer, axiom):
    dim = layer_dimension(layer)
    grid = [[DEFAULT_CHAR for _ in range(dim)] for _ in range(dim)]
    read_only = [[False for _ in range(dim)] for _ in range(dim)]

    if layer == 0:
        grid[0][0] = CENTER_CHAR
        read_only[0][0] = False
    else:
        ensure_layer_axiom(layer - 1, axiom)
        prev_grid, prev_read_only = data[(layer - 1, axiom)]
        prev_dim = layer_dimension(layer - 1)
        offset = (dim - prev_dim) // 2

        for py in range(prev_dim):
            for px in range(prev_dim):
                ch = prev_grid[py][px]
                if ch == CENTER_CHAR:
                    ch = ' '
                grid[py + offset][px + offset] = ch
                read_only[py + offset][px + offset] = True

    data[(layer, axiom)] = (grid, read_only)

def ensure_layer_axiom(layer, axiom):
    if (layer, axiom) not in data:
        create_layer_axiom(layer, axiom)

def get_outer_ring_cells(layer, axiom):
    """
    Return all non-empty (x,y,ch) in the outer ring,
    skipping ' ', '', or DEFAULT_CHAR.
    """
    grid, ro = data[(layer, axiom)]
    dim = layer_dimension(layer)
    center = layer
    if layer == 0:
        ch = grid[0][0]
        return [(0, 0, ch)]
    ring = []
    N = layer
    for y in range(-N, N + 1):
        for x in range(-N, N + 1):
            if max(abs(x), abs(y)) == N:
                gx = x + center
                gy = y + center
                ch = grid[gy][gx]
                # skip if it's default or blank
                if ch in [' ', '', DEFAULT_CHAR]:
                    continue
                ring.append((x, y, ch))
    return ring

# ---------------------------------------------------------------------
# 2) 3D RENDERING
# ---------------------------------------------------------------------
def perimeter_2d(shape, layer, fraction):
    if layer == 0:
        return (0, 0)
    if shape == "circle":
        r = layer
        theta = 2 * math.pi * fraction
        return (r * math.cos(theta), r * math.sin(theta))
    elif shape == "square":
        side = 2 * layer
        t = fraction % 1.0
        if t < 0.25:
            local = (t - 0.0) / 0.25
            return (-layer + local*side, layer)
        elif t < 0.5:
            local = (t - 0.25) / 0.25
            return (layer, layer - local*side)
        elif t < 0.75:
            local = (t - 0.5) / 0.25
            return (layer - local*side, -layer)
        else:
            local = (t - 0.75) / 0.25
            return (-layer, -layer + local*side)
    elif shape.startswith("polygon:"):
        # parse sides, fallback 6 if invalid
        N_str = shape.split(":", 1)[1]
        N = int(N_str) if N_str.isdigit() else 6
        total = fraction * N
        edge_index = int(math.floor(total))
        edge_fraction = total - edge_index
        angle1 = 2 * math.pi * edge_index / N
        angle2 = 2 * math.pi * ((edge_index + 1) % N) / N
        r = layer
        x1, y1 = (r * math.cos(angle1), r * math.sin(angle1))
        x2, y2 = (r * math.cos(angle2), r * math.sin(angle2))
        return (x1 + (x2 - x1) * edge_fraction,
                y1 + (y2 - y1) * edge_fraction)
    else:
        # fallback
        return (0, 0)

def calculate_coordinates(axiom, shape, layer, fraction):
    x2d, y2d = perimeter_2d(shape, layer, fraction)
    if axiom == 'A':  # XY plane
        return (x2d, y2d, 0)
    elif axiom == 'B':  # YZ plane
        return (0, x2d, y2d)
    elif axiom == 'C':  # XZ plane
        return (x2d, 0, y2d)
    elif axiom == 'D':
        factor = math.sqrt(2) / 2
        return (x2d, y2d*factor, y2d*factor)
    elif axiom == 'E':
        factor = math.sqrt(2) / 2
        return (y2d*factor, x2d, y2d*factor)
    elif axiom == 'F':
        factor = math.sqrt(2) / 2
        return (y2d*factor, y2d*factor, x2d)
    elif axiom == 'H':
        factor = math.sqrt(2) / 2
        return (x2d, y2d*factor, -y2d*factor)
    elif axiom == 'I':
        factor = math.sqrt(2) / 2
        return (-y2d*factor, x2d, y2d*factor)
    elif axiom == 'J':
        factor = math.sqrt(2) / 2
        return (-y2d*factor, y2d*factor, x2d)
    return (0, 0, 0)

def render_3d(filename=OUTPUT_FILENAME):
    """
    Create a 3D scatter trace for each layer & axiom’s ring,
    then write it to HTML.
    """
    layer_0_trace = {axiom: {'x': [], 'y': [], 'z': [], 'text': []} for axiom in AXIOM_CONFIGS}
    layer_1_trace = {axiom: {'x': [], 'y': [], 'z': [], 'text': []} for axiom in AXIOM_CONFIGS}
    layer_1_plus_traces = []

    if not data:
        fig = go.Figure()
        fig.write_html(filename)
        print(f"Visualization saved to {filename}. (no data yet)")
        return

    max_layer = max(layer for (layer, _) in data.keys())

    for (layer, axiom) in data.keys():
        ring_cells = get_outer_ring_cells(layer, axiom)
        if not ring_cells:
            continue

        # sort ring points by angle
        ring_cells.sort(key=lambda c: math.atan2(c[1], c[0]))
        x_vals, y_vals, z_vals, text_vals = [], [], [], []

        for i, (ox, oy, ch) in enumerate(ring_cells):
            fraction = i / len(ring_cells)
            x, y, z = calculate_coordinates(axiom, SHAPE, layer, fraction)
            x_vals.append(x)
            y_vals.append(y)
            z_vals.append(z)
            text_vals.append(ch)

        if len(x_vals) > 1:
            # close the loop visually
            x_vals.append(x_vals[0])
            y_vals.append(y_vals[0])
            z_vals.append(z_vals[0])
            text_vals.append(text_vals[0])

        if layer == 0:
            layer_0_trace[axiom]['x'].extend(x_vals)
            layer_0_trace[axiom]['y'].extend(y_vals)
            layer_0_trace[axiom]['z'].extend(z_vals)
            layer_0_trace[axiom]['text'].extend(text_vals)
        elif layer == 1:
            layer_1_trace[axiom]['x'].extend(x_vals)
            layer_1_trace[axiom]['y'].extend(y_vals)
            layer_1_trace[axiom]['z'].extend(z_vals)
            layer_1_trace[axiom]['text'].extend(text_vals)
        else:
            layer_1_plus_traces.append({
                'axiom': axiom,
                'layer': layer,
                'x': x_vals,
                'y': y_vals,
                'z': z_vals,
                'text': text_vals
            })

    fig = go.Figure()

    # layer_0
    for ax, config in AXIOM_CONFIGS.items():
        x_ = layer_0_trace[ax]['x']
        if x_:
            fig.add_trace(go.Scatter3d(
                x=x_,
                y=layer_0_trace[ax]['y'],
                z=layer_0_trace[ax]['z'],
                mode=LAYER_VISUALIZATION_MODES['layer_0'],
                text=layer_0_trace[ax]['text'],
                marker=dict(size=10, color=config['color'], symbol='circle'),
                opacity=LAYER0_OPACITY,
                name=f"Layer 0 - {config['label']}"
            ))

    # layer_1
    for ax, config in AXIOM_CONFIGS.items():
        x_ = layer_1_trace[ax]['x']
        if x_:
            fig.add_trace(go.Scatter3d(
                x=x_,
                y=layer_1_trace[ax]['y'],
                z=layer_1_trace[ax]['z'],
                mode=LAYER_VISUALIZATION_MODES['layer_1'],
                text=layer_1_trace[ax]['text'],
                marker=dict(size=8, color=config['color'], symbol='circle'),
                opacity=LAYER1_OPACITY,
                name=f"Layer 1 - {config['label']}"
            ))

    # layers 2+
    for trace in layer_1_plus_traces:
        config = AXIOM_CONFIGS[trace['axiom']]
        fig.add_trace(go.Scatter3d(
            x=trace['x'],
            y=trace['y'],
            z=trace['z'],
            mode=LAYER_VISUALIZATION_MODES['layer_1_plus'],
            text=trace['text'],
            marker=dict(size=5, color=config['color'], symbol='circle'),
            opacity=config['opacity'],
            name=f"Layer {trace['layer']} - {config['label']}"
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X", range=[-max_layer, max_layer]),
            yaxis=dict(title="Y", range=[-max_layer, max_layer]),
            zaxis=dict(title="Z", range=[-max_layer, max_layer]),
        ),
        title=f"3D Visualization ({SHAPE})",
        width=1000, height=800
    )
    fig.write_html(filename)
    print(f"Visualization saved to {filename}.")

# ---------------------------------------------------------------------
# 3) CURSOR / KEYBOARD HANDLERS
# ---------------------------------------------------------------------
def is_within_bounds(x, y):
    return (-current_layer <= x <= current_layer and -current_layer <= y <= current_layer)

def is_read_only(x, y):
    grid, ro = data[(current_layer, current_axiom)]
    center = current_layer
    gx = x + center
    gy = y + center
    return ro[gy][gx]

def jump_across(dx, dy):
    global cursor_x, cursor_y
    x, y = cursor_x, cursor_y
    while True:
        nx, ny = x + dx, y + dy
        if not is_within_bounds(nx, ny):
            return False
        if not is_read_only(nx, ny):
            cursor_x, cursor_y = nx, ny
            return True
        x, y = nx, ny

def move_cursor(dx, dy):
    jump_across(dx, dy)

def insert_char(ch):
    grid, read_only = data[(current_layer, current_axiom)]
    center = current_layer
    gx = cursor_x + center
    gy = cursor_y + center
    if not read_only[gy][gx]:
        grid[gy][gx] = ch

def go_to_layer_axiom(layer, axiom):
    global current_layer, current_axiom, cursor_x, cursor_y
    current_layer = layer
    current_axiom = axiom
    ensure_layer_axiom(current_layer, current_axiom)
    cursor_x, cursor_y = -current_layer, -current_layer

def draw_interface(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Layer: {current_layer}, Axiom: {current_axiom}, Pos=({cursor_x},{cursor_y}), Shape={SHAPE}")
    stdscr.addstr(1, 0, "F1=A, F2=B, F3=C, F4=D, F5=E, F6=F, F7=H, F8=I, F9=J | +/-=layers | Arrows=move | Type=insert")
    stdscr.addstr(2, 0, "Ctrl+D=exit, then check the .html. Prefill vs load is handled by arguments.")
    stdscr.addstr(3, 0, f"Press SHIFT or others for chars. Current fill_mode={FILL_MODE}.")

    grid, read_only = data[(current_layer, current_axiom)]
    dim = layer_dimension(current_layer)
    center = current_layer

    VIEW_RADIUS = 5
    min_xv = max(cursor_x - VIEW_RADIUS, -current_layer)
    max_xv = min(cursor_x + VIEW_RADIUS, current_layer)
    min_yv = max(cursor_y - VIEW_RADIUS, -current_layer)
    max_yv = min(cursor_y + VIEW_RADIUS, current_layer)

    offset_line = 5
    offset_col = 2

    for draw_y in range(min_yv, max_yv + 1):
        row_chars = []
        gy = draw_y + center
        for draw_x in range(min_xv, max_xv + 1):
            gx = draw_x + center
            ch = grid[gy][gx]
            display_char = ' ' if read_only[gy][gx] else ch

            if draw_x == cursor_x and draw_y == cursor_y:
                # highlight cursor
                if current_layer == 0 and current_axiom == 'A' and cursor_x == 0 and cursor_y == 0:
                    char = display_char
                else:
                    char = "▮" if display_char != DEFAULT_CHAR else "○"
            else:
                char = display_char
            row_chars.append(char)
        row_str = "".join(row_chars)
        stdscr.addstr(offset_line + (draw_y - min_yv), offset_col, row_str)

    stdscr.refresh()

# ---------------------------------------------------------------------
# 4) PREFILL
# ---------------------------------------------------------------------
def prefill_layers(mode, fillA, fillB, fillC, fillD, fillE, fillF, fillH, fillI, fillJ):
    """
    For each axiom, we get the fill list (like fillA).
    If that list has length M, we will fill up to layer=M
    (i.e. layers 1..M).
    """
    max_layers = max(len(fillA), len(fillB), len(fillC),
                     len(fillD), len(fillE), len(fillF),
                     len(fillH), len(fillI), len(fillJ))
    random.seed(0)

    axioms = ['A','B','C','D','E','F','H','I','J']
    fill_dict = {
        'A': fillA, 'B': fillB, 'C': fillC,
        'D': fillD, 'E': fillE, 'F': fillF,
        'H': fillH, 'I': fillI, 'J': fillJ
    }

    for layer in range(1, max_layers + 1):
        for axiom in axioms:
            ensure_layer_axiom(layer, axiom)
            grid, ro = data[(layer, axiom)]
            center = layer
            N = layer

            # gather ring coords
            ring_coords = []
            for y in range(-N, N + 1):
                for x in range(-N, N + 1):
                    if max(abs(x), abs(y)) == N:
                        gx = x + center
                        gy = y + center
                        if not ro[gy][gx]:
                            ring_coords.append((gx, gy))

            total = len(ring_coords)
            if total == 0:
                continue

            chars_list = fill_dict[axiom]
            base_char = None
            if layer <= len(chars_list):
                base_char = chars_list[layer-1].strip()  # remove extra spaces

            # apply the prefill mode
            if base_char and base_char != DEFAULT_CHAR:  # skip if empty
                if mode == 'full':
                    for (gx, gy) in ring_coords:
                        if base_char:
                            grid[gy][gx] = base_char
                elif mode == 'partial':
                    selected = random.sample(ring_coords, total//2)
                    for (gx, gy) in selected:
                        grid[gy][gx] = base_char
                elif mode == 'random':
                    # randomly fill half
                    selected = random.sample(ring_coords, total//2)
                    for (gx, gy) in selected:
                        # pick random from chars_list
                        ch = random.choice(chars_list)
                        ch = ch.strip()
                        if ch:
                            grid[gy][gx] = ch

# ---------------------------------------------------------------------
# 5) SAVE / LOAD
# ---------------------------------------------------------------------
def save_game_state(filename):
    """
    Save the entire `data` dict to a text file,
    including layer, axiom, dimension, and the entire grid.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Sort by layer, then axiom
        for (layer, axiom) in sorted(data.keys(), key=lambda x: (x[0], x[1])):
            grid, ro = data[(layer, axiom)]
            dim = layer_dimension(layer)
            f.write(f"BEGIN LAYER {layer} AXIOM {axiom} DIM {dim}\n")
            for row in grid:
                f.write("".join(row) + "\n")
            f.write("END LAYER\n")

def load_game_state(filename):
    """
    Load from file into `data`, ignoring read-only details
    (all become read_only=False).
    """
    data.clear()
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    idx = 0
    while idx < len(lines):
        line = lines[idx].rstrip('\n')
        if line.startswith("BEGIN LAYER"):
            parts = line.split()
            # e.g. "BEGIN LAYER 2 AXIOM C DIM 5"
            layer = int(parts[2])
            axiom = parts[4]
            dim = int(parts[6])
            idx += 1

            new_grid = []
            for _ in range(dim):
                row_str = lines[idx].rstrip('\n')
                new_grid.append(list(row_str))
                idx += 1

            # skip "END LAYER"
            idx += 1

            read_only = [[False]*dim for _ in range(dim)]
            data[(layer, axiom)] = (new_grid, read_only)
        else:
            idx += 1

# ---------------------------------------------------------------------
# 6) CURSES UI
# ---------------------------------------------------------------------
def run(stdscr):
    global current_layer, current_axiom
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    go_to_layer_axiom(0, 'A')

    while True:
        draw_interface(stdscr)
        key = stdscr.getch()
        if key == -1:
            continue

        # Ctrl+D => exit
        if key == 4:
            break

        if   key == curses.KEY_F1: go_to_layer_axiom(current_layer, 'A')
        elif key == curses.KEY_F2: go_to_layer_axiom(current_layer, 'B')
        elif key == curses.KEY_F3: go_to_layer_axiom(current_layer, 'C')
        elif key == curses.KEY_F4: go_to_layer_axiom(current_layer, 'D')
        elif key == curses.KEY_F5: go_to_layer_axiom(current_layer, 'E')
        elif key == curses.KEY_F6: go_to_layer_axiom(current_layer, 'F')
        elif key == curses.KEY_F7: go_to_layer_axiom(current_layer, 'H')
        elif key == curses.KEY_F8: go_to_layer_axiom(current_layer, 'I')
        elif key == curses.KEY_F9: go_to_layer_axiom(current_layer, 'J')
        elif key == ord('+'):
            go_to_layer_axiom(current_layer + 1, current_axiom)
        elif key == ord('-'):
            if current_layer > 0:
                go_to_layer_axiom(current_layer - 1, current_axiom)
        elif key == curses.KEY_LEFT:
            move_cursor(-1, 0)
        elif key == curses.KEY_RIGHT:
            move_cursor(1, 0)
        elif key == curses.KEY_UP:
            move_cursor(0, -1)
        elif key == curses.KEY_DOWN:
            move_cursor(0, 1)
        elif 32 <= key < 127:
            ch = chr(key)
            insert_char(ch)

# ---------------------------------------------------------------------
# 7) MAIN
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # parse arguments
    save_file = None
    load_file = None

    # Example usage of fills:
    #   --fillA=A, , , ,E --fillB=X,Y
    # We’ll store them in FILLS dict below.
    #   The key is the letter after '--fill'
    #   The value is a list of strings from splitting by comma.
    #
    # We also do a debug print to help you see how many items got parsed.
    for arg in sys.argv:
        if arg.startswith('--save='):
            save_file = arg.split('=')[1]
        elif arg.startswith('--load='):
            load_file = arg.split('=')[1]
        elif arg.startswith('--prefill'):
            PREFILL = True
        elif arg.startswith('--mode='):
            FILL_MODE = arg.split('=')[1]
        elif arg.startswith('--shape='):
            SHAPE = arg.split('=')[1]
        elif arg.startswith('--fill') and '=' in arg:
            # Something like '--fillA=' or '--fillB='
            # e.g. '--fillA=A, , ,C'
            # Extract the axiom letter(s) from the part after '--fill'.
            # E.g. '--fillA=' => key='A'
            fill_key = arg.split('=')[0][6:]  # everything after '--fill'
            fill_val_str = arg.split('=')[1]
            fill_list = fill_val_str.split(',')
            # Store in FILLS dict if valid
            if fill_key in FILLS:
                FILLS[fill_key] = fill_list
            print(f"DEBUG: fill{fill_key} = {FILLS[fill_key]} (length={len(FILLS[fill_key])})")

    # If --load is given, skip prefill
    if load_file and PREFILL:
        print("Cannot use --load and --prefill together, ignoring prefill.")
        PREFILL = False

    # load or prefill
    if load_file:
        load_game_state(load_file)
    elif PREFILL:
        # each fill is passed individually
        prefill_layers(
            FILL_MODE,
            FILLS['A'], FILLS['B'], FILLS['C'],
            FILLS['D'], FILLS['E'], FILLS['F'],
            FILLS['H'], FILLS['I'], FILLS['J']
        )

    # run the curses UI
    try:
        curses.wrapper(run)
        # after exiting the UI, do 3D rendering
        render_3d()
    except KeyboardInterrupt:
        pass

    print("Exited.")

    # if we have --save=..., save the data
    if save_file:
        save_game_state(save_file)
        print(f"Saved data to {save_file}.")
