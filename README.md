# Task Prioritization & Analysis System

A comprehensive task management and analysis system powered by AI, designed to help developers prioritize work, understand dependencies, and plan sprints effectively.

## 🌟 Features

### 1. **AI-Powered Task Parsing**
- Upload tasks in any format (TXT, CSV, JSON, Excel, Markdown)
- Automatic extraction of task details using Ollama AI
- Intelligent parsing of unstructured task descriptions

### 2. **Manual Task Entry**
- Intuitive form-based task input
- Support for priorities, dependencies, labels, and effort estimates
- Real-time validation and dependency management

### 3. **Comprehensive Task Analysis**
- **Dependency Analysis**: Detect circular dependencies and calculate execution order
- **Risk Assessment**: Identify high-risk tasks based on complexity, dependencies, and priority
- **Sprint Planning**: Automatic sprint recommendations with balanced workload
- **Parallel Opportunities**: Find tasks that can be executed simultaneously
- **Technology Mapping**: Group tasks by required technologies and skills

### 4. **Beautiful Visualizations**
- Interactive dependency graphs using Plotly
- Timeline and Gantt charts for project planning
- Risk assessment charts with detailed breakdowns
- Sprint planning timelines

### 5. **Bob AI Custom Mode**
- Integrated custom mode for Bob IDE
- Step-by-step task guidance
- Visual flow diagram generation
- Export analysis results

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama with qwen2.5:7b model (for AI parsing)
- Graphviz (optional, for PNG diagram generation)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd IBM_BOB
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**
- Windows: `.venv\Scripts\activate`
- macOS/Linux: `source .venv/bin/activate`

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Install Ollama (for AI parsing)**
- Download from: https://ollama.ai
- Pull the model: `ollama pull qwen2.5:7b`

6. **Install Graphviz (optional)**
- Windows: Download from https://graphviz.org/download/
- macOS: `brew install graphviz`
- Linux: `sudo apt-get install graphviz`

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Tab 1: Upload & Parse

1. **Upload a file** containing your tasks (any format)
2. Click **"Parse with AI"** to extract tasks automatically
3. Review the parsed tasks
4. Click **"Add All to Task List"** to import them

**Supported Formats:**
- **Text files**: Plain text with task descriptions
- **CSV**: Structured task data
- **JSON**: Task objects with properties
- **Excel**: Spreadsheets with task information
- **Markdown**: Task lists in markdown format

### Tab 2: Manual Entry

1. Fill in the task form:
   - Title (required)
   - Description (required)
   - Priority (high/medium/low)
   - Status (pending/in-progress/completed)
   - Estimated effort
   - Labels (comma-separated)
   - Dependencies (select from existing tasks)
   - Notes

2. Click **"Add Task"** to save

### Tab 3: Task List

- View all tasks with filtering options
- Filter by priority, status, or search terms
- Edit or delete tasks
- See task dependencies and relationships

### Tab 4: Analysis Results

1. Click **"Run Analysis"** to analyze all tasks
2. Explore four analysis tabs:

   **📊 Summary**
   - Total tasks and distribution
   - Priority and status breakdown

   **🔗 Dependencies**
   - Interactive dependency graph
   - Execution order recommendations
   - Parallel execution opportunities
   - Circular dependency detection

   **⚠️ Risk Assessment**
   - Visual risk charts
   - Detailed risk factors for each task
   - Risk level indicators (High/Medium/Low)

   **🏃 Sprint Planning**
   - Recommended sprint breakdown
   - Effort distribution per sprint
   - Technology and skill dependencies

3. **Export** analysis results as JSON

## 🤖 Bob AI Custom Mode

### Installation

1. Copy the custom mode file:
```bash
cp bob-custom-modes/task-prioritizer-export.yaml ~/.bob/custom-modes/
```

2. Restart Bob IDE

3. Select "Task Prioritizer" from custom modes

### Usage

1. Export tasks from the Streamlit app (JSON format)
2. Open Bob IDE and select "Task Prioritizer" mode
3. Paste the exported JSON
4. Bob will analyze and provide step-by-step guidance

### Features

- Dependency analysis
- Execution order recommendations
- Risk assessment
- Sprint planning suggestions
- Visual flow diagram generation (requires Graphviz)

## 📁 Project Structure

```
IBM_BOB/
├── app.py                      # Main Streamlit application
├── models.py                   # Task and TaskCollection dataclasses
├── storage.py                  # JSON persistence and LLM export
├── ai_parser.py               # AI-powered task parser (Ollama)
├── analyzer.py                # Task analysis engine
├── visualizations.py          # Plotly visualization components
├── generate_diagram.py        # PNG flow diagram generator
├── requirements.txt           # Python dependencies
├── bob-custom-modes/          # Bob IDE custom mode files
│   ├── task-prioritizer-export.yaml
│   ├── QUICK_START.md
│   └── DIAGRAM_SETUP.md
├── output/                    # Generated diagrams and exports
└── README.md                  # This file
```

## 🔧 Configuration

### Ollama Settings

The AI parser uses Ollama with the qwen2.5:7b model. You can configure:

- **Model**: Change in `ai_parser.py` (line 15)
- **API URL**: Default is `http://localhost:11434`
- **Temperature**: Adjust for more/less creative parsing

### Analysis Settings

Customize analysis parameters in `analyzer.py`:

- **Sprint capacity**: Default 10 story points per sprint
- **Risk thresholds**: Adjust risk level calculations
- **Dependency depth**: Maximum allowed dependency chain

## 📊 Data Format

### Task Structure

```json
{
  "id": "unique-task-id",
  "title": "Task title",
  "description": "Detailed description",
  "priority": "high|medium|low",
  "status": "pending|in-progress|completed",
  "estimated_effort": "2 hours",
  "labels": ["frontend", "api"],
  "dependencies": ["other-task-id"],
  "notes": "Additional notes",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Export Formats

- **JSON**: Full task data with metadata
- **LLM Export**: Optimized text format for AI analysis
- **Analysis Report**: Complete analysis results with visualizations

## 🎯 Best Practices

1. **Define Dependencies Early**: Set up task dependencies before running analysis
2. **Use Meaningful Labels**: Labels help with technology mapping and risk assessment
3. **Estimate Effort**: Provide effort estimates for better sprint planning
4. **Regular Analysis**: Re-run analysis as tasks progress
5. **Review Risks**: Pay attention to high-risk tasks and plan accordingly

## 🐛 Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve
```

### Graphviz Not Found

```bash
# Windows: Add Graphviz to PATH
# macOS: brew install graphviz
# Linux: sudo apt-get install graphviz
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Ollama](https://ollama.ai/)
- Visualizations by [Plotly](https://plotly.com/)
- Diagrams by [Graphviz](https://graphviz.org/)
- Network analysis by [NetworkX](https://networkx.org/)

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ by Bob AI**