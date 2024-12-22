# Layer Axiom Game

**Layer Axiom Game** is a console-based interactive game that allows you to navigate and manipulate layered grids with custom axioms, visualizing their structure in 2D and rendering them in 3D using Plotly.

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
python layer_axiom_game.py --prefill --fillA=X,Y,Z --fillB=A,B --mode=random
```

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