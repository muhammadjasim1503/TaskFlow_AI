# Setting Up Visual Diagram Generation

The Task Prioritizer mode can generate visual flow diagrams as PNG images showing task dependencies and execution order.

## Prerequisites

### 1. Install Python graphviz Library

```bash
# Activate your virtual environment first
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install the graphviz Python package
pip install graphviz
```

### 2. Install Graphviz System Package

The Python library requires the Graphviz system software to be installed:

#### Windows
1. Download installer from: https://graphviz.org/download/
2. Run the installer
3. **Important**: Add Graphviz to your PATH during installation
4. Or manually add `C:\Program Files\Graphviz\bin` to your system PATH
5. Restart your terminal/IDE after installation

#### macOS
```bash
brew install graphviz
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install graphviz
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install graphviz
```

### 3. Verify Installation

```bash
# Check if graphviz command is available
dot -V

# Should output something like: dot - graphviz version 2.50.0
```

## How It Works

When you use the Task Prioritizer mode in Bob:

1. **Bob analyzes your tasks** and provides text-based guidance
2. **Bob saves task data** to `output/temp_tasks.json`
3. **Bob runs the diagram script**: `python generate_diagram.py output/temp_tasks.json output/task-flow-diagram.png`
4. **A PNG image is created** at `output/task-flow-diagram.png`

## Diagram Features

The generated diagram shows:

- ✅ **Task boxes** with titles, priorities, and effort estimates
- ✅ **Color coding** by priority:
  - 🔴 Red = High priority
  - 🟡 Yellow = Medium priority
  - 🟢 Green = Low priority
- ✅ **Arrows** showing dependencies between tasks
- ✅ **Visual flow** from start to finish
- ✅ **Professional layout** using Graphviz's automatic positioning

## Manual Diagram Generation

You can also generate diagrams manually:

```bash
# From your project root directory
python generate_diagram.py data/tasks.json output/my-diagram.png
```

## Troubleshooting

### Error: "graphviz library is required"
```bash
pip install graphviz
```

### Error: "failed to execute 'dot'"
- Graphviz system package is not installed or not in PATH
- Follow the installation steps above for your OS
- Restart your terminal after installation

### Error: "File not found"
- Make sure you're running from the project root directory
- Check that the input JSON file exists

### Diagram not generating in Bob mode
1. Verify Graphviz is installed: `dot -V`
2. Check that `generate_diagram.py` exists in project root
3. Ensure Bob has execute_command permissions
4. Check Bob's console for error messages

## Example Output

The diagram will look like this:

```
┌─────────────────────────────┐
│ Setup Database              │
│ Priority: HIGH              │
│ Effort: 3 days              │
└─────────────┬───────────────┘
              │
              ├──────────────┬──────────────┐
              ▼              ▼              ▼
┌─────────────────┐  ┌─────────────┐  ┌──────────┐
│ Auth API        │  │ Product API │  │ ...      │
│ Priority: HIGH  │  │ Priority: HIGH│  │          │
│ Effort: 5 days  │  │ Effort: 4 days│  │          │
└─────────────────┘  └─────────────┘  └──────────┘
```

(Actual output is a professional PNG image with colors and proper layout)

## Integration with Streamlit App

The Streamlit app saves tasks to `data/tasks.json`. You can generate a diagram from this:

```bash
python generate_diagram.py data/tasks.json output/current-tasks-diagram.png
```

## Tips

1. **Keep task titles short** for better diagram readability
2. **Use clear dependencies** - the diagram shows these as arrows
3. **Review the diagram** to spot missing dependencies or circular references
4. **Share the PNG** with your team for sprint planning discussions

---

**Need Help?**
- Check that all prerequisites are installed
- Verify the JSON file format matches the expected structure
- See `generate_diagram.py` for the expected data format