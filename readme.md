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

4. **Stunning 3D Visualizations**
   - Render layered grids in 3D with customizable perspectives.
   - Export interactive visualizations as HTML files.

5. **Prefill Mode**
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
- `--prefill`: Prefill layers with default or custom patterns.
- `--fillX=<values>`: Specify custom fill characters for axiom X (e.g., `--fillA=X,Y,Z`).
- `--mode=<mode>`: Choose prefill mode (`full`, `partial`, `random`).

### Example
```bash
python layer_axiom_game.py --prefill --fillA=X,Y,Z --fillB=A,B --mode=full
```

---

## ⚙️ Configuration Options

### 1. Visualization Modes
Define how each layer is rendered:
- **Options**: `lines`, `markers`, `text`, `markers+lines`
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

Start the game:
```bash
python layer_axiom_game.py
```

Navigate the grid, switch axioms, and add characters to experiment with different grid behaviors.

### View the 3D Visualization
```bash
open matrix_visualization.html
```

---

## ✨ Explore, Create, Visualize!

Unleash your creativity and dive into the world of layered grids and axioms. Enjoy the journey! 🎮