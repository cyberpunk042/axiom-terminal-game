# Axioms & Layers Simulation "Game"

**Layered Axioms Simulation** is a console-based interactive game that allows you to navigate and manipulate layered grids with custom axioms, visualizing their structure in 2D and rendering them in 3D using Plotly.

---

## Features

1. **Layer-Based Grids**:
   - Create and interact with layers of grids, where each layer is defined by an axiom.
   - Layers expand dynamically based on user input.

2. **Cursor Navigation**:
   - Move the cursor across the grid using arrow keys.
   - Jump across read-only cells to interact with editable cells.

3. **Axiom Types**:
   - Multiple axiom types (`A`, `B`, `C`, `D`, `E`, `F`, `H`, `I`, `J`) define unique grid behaviors and orientations.
   - Axioms are visualized in both 2D and 3D.

4. **3D Visualization**:
   - Render the layered grid in 3D with different planes and perspectives.
   - Export the visualization as an interactive HTML file.

5. **Prefill Mode**:
   - Automatically populate layers with predefined characters or randomized patterns for quicker exploration.

---

## Controls

### Navigation
- **Arrow Keys**: Move the cursor across the grid.
- **`+` / `-`**: Navigate between layers.
- **`Ctrl+D`**: Exit the game.

### Axiom Switching
- **`F1` to `F9`**: Switch between axioms `A` to `J`.

### Grid Interaction
- **Type Characters**: Insert characters at the cursor's position (if editable).

---

## Requirements

- Python 3.8+
- Required libraries: `curses`, `plotly`, `logging`, `math`, `random`

Install dependencies:
```bash
pip install plotly
```

Running the Game
Run the game with the following command:

```bash
python layer_axiom_game.py
```
### Optional Arguments
--prefill: Prefill layers with default or custom patterns.
--fillX=<values>: Specify custom fill characters for axiom X (e.g., --fillA=X,Y,Z).
--mode=<mode>: Set the prefill mode (full, partial, random).

## Example:
```bash
python layer_axiom_game.py --prefill --fillA=X,Y,Z --fillB=A,B --mode=full
```

## Configuration Options

### 1. Visualization Modes
Control how each layer is rendered. Set modes for:
- **Layer 0**
- **Layer 1**
- **Layer 1+**

Options:
- `lines`: Draw only lines connecting points.
- `markers`: Show only markers (points).
- `text`: Show only labels or text.
- `markers+lines`: Combine markers and lines.

### 2. Axiom Settings
Customize visualization for each axiom (`A`, `B`, `C`, etc.). Configure:
- **Color**: The color used for rendering.
- **Label**: A descriptive name for the axiom.
- **Opacity**: Transparency level for each axiom.

### 3. General Configurations
Set overall visualization preferences:
- **Default Character**: The placeholder for empty cells.
- **Center Character**: The character representing the center of layers.
- **Opacity Values**: Adjust the transparency of the axiom layers.

---

### 3D Visualization
The 3D visualization of the grid is exported to matrix_visualization.html. Open the file in a web browser to explore the rendered layers interactively.

### Logging
All game events and interactions are logged in layer_axiom_game.log for debugging and analysis.

## Example Usage
Start the game:
```bash
python layer_axiom_game.py
```

Move the cursor, switch axioms, and add characters to explore grid behavior.

### View the generated 3D visualization:
```bash
open matrix_visualization.html
```

Enjoy experimenting with layered grids and axioms! 🎮