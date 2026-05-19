# Bob Custom Mode: Task Prioritizer

A specialized Bob AI mode for analyzing development tasks and providing step-by-step execution guidance.

## 📋 Overview

The **Task Prioritizer** mode transforms Bob into an expert project manager that analyzes your development tasks and tells you exactly which task to do first, second, third, and so on - with clear reasoning for each step.

## ✨ Features

- **Dependency Analysis** - Identifies all task relationships and prerequisites
- **Optimal Sequencing** - Determines the best execution order using graph algorithms
- **Step-by-Step Guidance** - Provides numbered, actionable task list
- **Risk Assessment** - Flags complex or risky tasks
- **Parallel Work Detection** - Identifies tasks that can be done simultaneously
- **Sprint Planning** - Groups tasks into logical milestones
- **Clear Reasoning** - Explains WHY each task should be done in that order

## 🚀 Installation

### Method 1: Manual Installation (Recommended)

1. **Locate Bob's Custom Modes Directory**
   - Windows: `%APPDATA%\Bob\custom-modes\`
   - macOS: `~/Library/Application Support/Bob/custom-modes/`
   - Linux: `~/.config/Bob/custom-modes/`

2. **Copy the Mode File**
   ```bash
   # Copy task-prioritizer.json to Bob's custom modes directory
   cp bob-custom-modes/task-prioritizer.json [Bob-custom-modes-directory]/
   ```

3. **Restart Bob** (if running)

4. **Verify Installation**
   - Open Bob
   - Look for "Task Prioritizer" mode in the mode selector
   - Icon should be 📋

### Method 2: Import via Bob UI

1. Open Bob
2. Go to Settings → Custom Modes
3. Click "Import Mode"
4. Select `task-prioritizer.json`
5. Confirm import

## 📖 How to Use

### Basic Workflow

1. **Export Tasks from the Task Input System**
   ```
   - Open the Streamlit app (http://localhost:8501)
   - Add your development tasks
   - Click "Export for LLM Analysis" in sidebar
   - Download tasks_for_llm.txt
   ```

2. **Switch to Task Prioritizer Mode**
   ```
   - Open Bob
   - Select "Task Prioritizer" mode from dropdown
   - You'll see the 📋 icon
   ```

3. **Upload Your Tasks**
   ```
   - Click the attachment icon
   - Upload tasks_for_llm.txt
   - Or paste the content directly
   ```

4. **Get Your Execution Plan**
   ```
   - Bob will automatically analyze the tasks
   - You'll receive a numbered, step-by-step plan
   - Each step includes reasoning and dependencies
   ```

### Example Usage

**Input:**
```
Upload tasks_for_llm.txt containing:
- Setup Database Schema
- Create API Endpoints
- Build User Interface
- Write Unit Tests
- Deploy to Production
```

**Output from Task Prioritizer:**
```
📊 TASK ANALYSIS SUMMARY
- Total tasks: 5
- Dependencies: Database → API → UI → Tests → Deploy
- Critical path: All sequential
- Timeline: ~3 weeks

🎯 STEP-BY-STEP EXECUTION PLAN

STEP 1: Setup Database Schema
Priority: HIGH
Effort: 2 days

WHY THIS STEP:
Foundation for entire application. No other work can proceed 
without database structure in place.

DEPENDENCIES: None
BLOCKERS: None
PARALLEL OPPORTUNITIES: Can start planning API design
NEXT STEPS: Enables API development

---

STEP 2: Create API Endpoints
Priority: HIGH
Effort: 5 days

WHY THIS STEP:
Depends on database. Required by frontend. Core business logic.

DEPENDENCIES: Database schema must be complete
BLOCKERS: None if database is ready
PARALLEL OPPORTUNITIES: Can start UI mockups
NEXT STEPS: Enables frontend development

[... continues for all tasks ...]
```

## 🎯 Use Cases

### 1. Daily Planning
```
"What should I work on today?"
→ Upload your tasks
→ Get prioritized list for the day
```

### 2. Sprint Planning
```
"Organize these tasks into 2-week sprints"
→ Use "Sprint Planning" shortcut
→ Get sprint breakdown with goals
```

### 3. Dependency Review
```
"Check if I'm missing any dependencies"
→ Use "Dependency Review" shortcut
→ Get analysis of task relationships
```

### 4. Quick Priority Check
```
"Quick list of what to do first"
→ Use "Quick Priority Check" shortcut
→ Get condensed priority list
```

## 🔧 Available Shortcuts

The mode includes pre-configured shortcuts:

1. **Analyze Tasks** - Full detailed analysis
2. **Quick Priority Check** - Fast numbered list
3. **Dependency Review** - Focus on dependencies
4. **Sprint Planning** - Group into sprints

Access shortcuts via the shortcuts menu in Bob.

## 📝 Tips for Best Results

### 1. Provide Complete Information
- Fill in all task fields (title, description, priority, effort)
- Mark all dependencies explicitly
- Add notes for context

### 2. Be Specific in Descriptions
```
❌ Bad: "Fix bug"
✅ Good: "Fix authentication timeout bug in login API endpoint"
```

### 3. Use Realistic Effort Estimates
```
✅ "2 hours", "3 days", "5 story points"
❌ "quick", "soon", "not sure"
```

### 4. Mark Dependencies Clearly
- Use the dependency selector in the Task Input System
- Don't rely on implicit dependencies

### 5. Update and Re-analyze
- As tasks complete, update status
- Re-export and re-analyze
- Adjust plan based on new information

## 🎨 Customization

You can customize the mode by editing `task-prioritizer.json`:

### Adjust Temperature
```json
"temperature": 0.7  // Lower = more consistent, Higher = more creative
```

### Modify System Prompt
Edit the `systemPrompt` field to change behavior:
- Add industry-specific considerations
- Include team-specific guidelines
- Adjust output format preferences

### Add Custom Shortcuts
```json
{
  "name": "My Custom Analysis",
  "description": "Custom analysis type",
  "prompt": "Your custom prompt here"
}
```

## 🔍 Understanding the Output

### Task Analysis Summary
- Overview of total tasks and relationships
- Critical path identification
- Timeline estimates

### Issues Detected
- Circular dependencies (A→B→C→A)
- Missing dependencies
- Unclear or risky tasks
- Recommendations for fixes

### Step-by-Step Plan
Each step includes:
- **Task Title & ID** - What to work on
- **Priority & Effort** - Importance and time needed
- **Why This Step** - Reasoning for the order
- **Dependencies** - What must be done first
- **Blockers** - Potential issues
- **Parallel Opportunities** - What else can be done
- **Next Steps** - What this enables

### Sprint Recommendations
- Logical groupings of tasks
- Sprint goals and themes
- Timeline estimates
- Resource considerations

### Optimization Suggestions
- Ways to improve efficiency
- Tasks that could be combined
- Technical debt considerations

## 🐛 Troubleshooting

### Mode Not Appearing
1. Check file is in correct directory
2. Verify JSON syntax is valid
3. Restart Bob completely
4. Check Bob logs for errors

### Analysis Seems Generic
1. Provide more detailed task descriptions
2. Mark all dependencies explicitly
3. Add context in notes field
4. Use specific effort estimates

### Circular Dependencies Detected
1. Review the flagged tasks
2. Break the cycle by removing one dependency
3. Consider if tasks should be combined
4. Re-export and re-analyze

### Missing Dependencies Not Found
1. Be more explicit in task descriptions
2. Add technical context in notes
3. Ask Bob to review specific task pairs
4. Manually add missing dependencies

## 📊 Example Scenarios

### Scenario 1: New Feature Development
```
Tasks:
- Design database schema
- Create API endpoints
- Build React components
- Write integration tests
- Update documentation

Result:
STEP 1: Design database schema (foundation)
STEP 2: Create API endpoints (depends on DB)
STEP 3: Build React components (depends on API)
STEP 4: Write integration tests (depends on components)
STEP 5: Update documentation (can be parallel with tests)
```

### Scenario 2: Bug Fixes
```
Tasks:
- Fix critical payment bug (HIGH)
- Fix UI alignment issue (LOW)
- Fix email notification bug (MEDIUM)

Result:
STEP 1: Fix critical payment bug (HIGH priority, business impact)
STEP 2: Fix email notification bug (MEDIUM priority)
STEP 3: Fix UI alignment issue (LOW priority, cosmetic)
```

### Scenario 3: Refactoring Project
```
Tasks:
- Extract shared utilities
- Refactor authentication module
- Update tests
- Migrate to new API

Result:
STEP 1: Extract shared utilities (enables other refactoring)
STEP 2: Refactor authentication (depends on utilities)
STEP 3: Migrate to new API (depends on auth refactor)
STEP 4: Update tests (after all changes complete)
```

## 🔄 Integration with Task Input System

The Task Prioritizer mode is designed to work seamlessly with the Task Input & Storage System:

1. **Add tasks** in Streamlit app
2. **Export** using "Export for LLM Analysis"
3. **Upload** to Bob in Task Prioritizer mode
4. **Get guidance** on execution order
5. **Update status** as you complete tasks
6. **Re-export and re-analyze** regularly

## 🚀 Advanced Usage

### Iterative Planning
```
1. Get initial plan from Task Prioritizer
2. Complete first few tasks
3. Update task status in Streamlit app
4. Re-export and upload to Bob
5. Get updated plan for remaining tasks
```

### Team Coordination
```
1. Export team's task list
2. Use Task Prioritizer to identify parallel work
3. Assign tasks based on dependencies
4. Share execution plan with team
```

### Risk Management
```
1. Upload all project tasks
2. Ask: "Which tasks are highest risk?"
3. Get risk assessment and mitigation strategies
4. Prioritize risky tasks early
```

## 📚 Additional Resources

- **Main Documentation**: See `README.md` in project root
- **Bob Integration Guide**: See `BOB_CUSTOM_MODE_GUIDE.md`
- **Task Input System**: See Streamlit app documentation

## 🤝 Support

For issues or questions:
1. Check this README
2. Review example scenarios
3. Test with sample data
4. Check Bob's custom mode documentation

## 📄 License

This custom mode is part of the Task Input & Storage System project.

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-17  
**Compatibility**: Bob AI Assistant (all versions with custom mode support)