# Axioms & Layers Simulation "Game"

**Layered Axioms Simulation** is an interactive console-based game where you explore and manipulate layered grids defined by custom axioms. Visualize your creations in 2D and 3D with **Plotly**, combining the power of grids and geometry for a unique simulation experience.

---

## 🌟 Features

1. **Dynamic Layered Grids**
   - Create and interact with layered grids, each governed by unique axioms.
   - Layers dynamically expand based on user input.

2. **Intuitive Cursor Navigation**
   - Seamlessly move across the grid using arrow keys.
   - Interact with editable cells while skipping read-only ones.

3. **Customizable Axioms**
   - Choose from a variety of axiom types (`A`, `B`, `C`, `D`, `E`, `F`, `H`, `I`, `J`).
   - Each axiom offers distinct grid behaviors and visual styles.

4. **Customizable Shapes**
   - Generate grids based on different perimeter shapes:
     - **Circle** (default): Smooth radial grids.
     - **Square**: Geometric, angular grids.
     - **Polygon:N**: Specify `N` sides for complex shapes (e.g., hexagon, dodecagon).

5. **Save & Load Game States**
   - Save your current game state to a file using `--save=<filename>`.
   - Reload and continue from a saved state with `--load=<filename>`.
   - Consistent read-only navigation whether layers are freshly created or loaded.

6. **Stunning 3D Visualizations**
   - Render layered grids in 3D with customizable perspectives.
   - Export interactive visualizations as HTML files.

7. **Prefill Mode**
   - Quickly populate grids with predefined patterns or randomized characters for faster exploration.

---

## 🎮 Controls

### Navigation
- **Arrow Keys**: Move the cursor.
- **`+` / `-`**: Switch between layers.
- **`Ctrl+D`**: Exit the game.

### Axiom Switching
- **`F1` to `F9`**: Toggle between axioms `A` to `J`.

### Grid Interaction
- **Type Characters**: Add characters at the cursor's position (if editable).

---

## 🔧 Requirements

- Python 3.8+
- Libraries: `curses`, `plotly`, `logging`, `math`, `random`

Install dependencies:
```bash
pip install plotly
```

---

## 🚀 Getting Started

Run the game with:
```bash
python layer_axiom_game.py
```

### Optional Arguments
- `--shape=<shape>`: Specify the perimeter shape for grids:
  - `circle` (default): Radial grids.
  - `square`: Square perimeter grids.
  - `polygon:N`: N-sided polygon grids (e.g., `polygon:6` for a hexagon).
- `--prefill`: Prefill layers with default or custom patterns.
- `--fillX=<values>`: Specify custom fill characters for axiom X (e.g., `--fillA=X,Y,Z`).
- `--mode=<mode>`: Choose prefill mode (`full`, `partial`, `random`).
- `--save=<filename>`: Save the current game state to a file.
- `--load=<filename>`: Load a previously saved game state.

### Examples

#### Start with a Custom Shape
```bash
python layer_axiom_game.py --shape=square --prefill --fillA=X,Y,Z --fillB=A,B --mode=full
```

#### Save Your Progress
```bash
python layer_axiom_game.py --shape=circle --save=game_state.txt
```

#### Reload and Continue
```bash
python layer_axiom_game.py --load=game_state.txt
```

---

## ⚙️ Configuration Options

### 1. Visualization Modes
Define how each layer is rendered:
- **Options**: `lines`, `markers`, `text`, `lines+markers`
- Configure modes for specific layers (e.g., `Layer 0`, `Layer 1+`).

### 2. Axiom Settings
Customize the appearance for each axiom:
- **Color**: Choose rendering colors.
- **Label**: Assign descriptive names.
- **Opacity**: Adjust transparency.

### 3. General Settings
Set overall preferences:
- **Default Character**: Placeholder for empty cells.
- **Center Character**: Representation of the layer center.
- **Opacity**: Adjust transparency levels for layers.

---

## 🌌 3D Visualization

- The 3D grid visualization is exported as `matrix_visualization.html`.
- Open the file in any web browser for an interactive exploration of layered grids.

---

## 🛠️ Logging

- Game events and interactions are logged in `layer_axiom_game.log` for debugging and analysis.

---

## 📖 Example Usage

### Generate a Complex Grid
```bash
python layer_axiom_game.py --shape=polygon:12 --prefill --fillA=X --fillB=Y --fillC=Z --mode=partial
```

### Save and Reload
Save the game state:
```bash
python layer_axiom_game.py --shape=circle --save=my_game.txt
```

Reload the saved state:
```bash
python layer_axiom_game.py --load=my_game.txt
```

### View the 3D Visualization
After exiting, open the exported visualization:
```bash
open matrix_visualization.html
```

---

## ✨ Explore, Create, Visualize!

Unleash your creativity and dive into the world of layered grids and axioms. Whether exploring radial grids, polygons, or saving and reloading intricate designs, this game offers endless possibilities for simulation and visualization. Enjoy the journey! 🎮
