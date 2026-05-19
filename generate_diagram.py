"""
Script to generate task flow diagrams as images.
Requires: graphviz, pillow
"""
import json
import os
from pathlib import Path

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Warning: graphviz not installed. Install with: pip install graphviz")


def generate_task_diagram(tasks_data, output_path="output/task-flow-diagram.png"):
    """
    Generate a visual task flow diagram from task data.
    
    Args:
        tasks_data: Dictionary containing task information
        output_path: Path where the diagram image will be saved
    """
    if not GRAPHVIZ_AVAILABLE:
        print("ERROR: graphviz library is required to generate diagrams")
        print("Install with: pip install graphviz")
        print("Also install Graphviz system package:")
        print("  - Windows: Download from https://graphviz.org/download/")
        print("  - macOS: brew install graphviz")
        print("  - Linux: sudo apt-get install graphviz")
        return False
    
    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Create a new directed graph
    dot = Digraph(comment='Task Flow Diagram')
    dot.attr(rankdir='TB', size='12,12')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    
    # Priority colors
    priority_colors = {
        'high': '#ff6b6b',      # Red
        'medium': '#ffd93d',    # Yellow
        'low': '#6bcf7f'        # Green
    }
    
    # Parse tasks
    tasks = tasks_data.get('tasks', [])
    
    # Add nodes
    for task in tasks:
        task_id = task.get('id', '')
        title = task.get('title', 'Untitled')
        priority = task.get('priority', 'medium').lower()
        effort = task.get('estimated_effort', 'Unknown')
        
        # Create label
        label = f"{title}\n"
        label += f"Priority: {priority.upper()}\n"
        label += f"Effort: {effort}"
        
        # Get color based on priority
        color = priority_colors.get(priority, '#cccccc')
        
        # Add node
        dot.node(task_id[:8], label, fillcolor=color, fontcolor='white' if priority == 'high' else 'black')
    
    # Add edges (dependencies)
    for task in tasks:
        task_id = task.get('id', '')
        dependencies = task.get('dependencies', [])
        
        for dep_id in dependencies:
            # Add edge from dependency to task
            dot.edge(dep_id[:8], task_id[:8])
    
    # Render the diagram
    try:
        # Remove extension from output_path for graphviz
        output_base = str(Path(output_path).with_suffix(''))
        dot.render(output_base, format='png', cleanup=True)
        print(f"[SUCCESS] Diagram generated successfully: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Error generating diagram: {e}")
        return False


def generate_from_json_file(json_path, output_path="output/task-flow-diagram.png"):
    """
    Generate diagram from a JSON file containing tasks.
    
    Args:
        json_path: Path to JSON file with task data
        output_path: Path where the diagram image will be saved
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return generate_task_diagram(data, output_path)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {json_path}")
        return False
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON in file: {json_path}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_diagram.py <path_to_tasks.json> [output_path]")
        print("Example: python generate_diagram.py data/tasks.json output/diagram.png")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output/task-flow-diagram.png"
    
    success = generate_from_json_file(json_path, output_path)
    sys.exit(0 if success else 1)

# Made with Bob
