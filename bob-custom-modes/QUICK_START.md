# Quick Start: Installing Task Prioritizer Mode in Bob IDE

## For Bob IDE Users (YAML Import)

Bob IDE requires a specific YAML format for custom modes. Follow these simple steps:

### Step 1: Import the Mode

1. **Open Bob IDE**
2. **Find the Import Option**:
   - Look for "Custom Modes" section
   - Or click the "+" button to add a new mode
   - Or go to Settings → Custom Modes → Import

3. **Select the CORRECT YAML File**:
   - Navigate to: `bob-custom-modes/task-prioritizer-export.yaml` ⭐
   - **Important:** Use `task-prioritizer-export.yaml`, NOT `task-prioritizer.yaml`
   - This file uses Bob IDE's required format with `customModes:` structure
   - Click "Import" or "Open"

4. **Confirm Import**:
   - The mode should now appear in your mode list
   - Look for "📋 Task Prioritizer"

### Step 2: Test It

1. **Switch to Task Prioritizer Mode**:
   - Select "📋 Task Prioritizer" from the mode dropdown

2. **Upload Sample Tasks**:
   - Use the provided `sample-tasks-for-testing.txt` file
   - Or paste this quick test:
   ```
   I have 3 tasks:
   1. Setup database (no dependencies)
   2. Create API (depends on database)
   3. Build frontend (depends on API)
   
   What order should I do them in?
   ```

3. **Get Your Analysis**:
   - Bob will provide step-by-step guidance
   - You'll see task order with clear reasoning

### Step 3: Use with Your Tasks

1. **Add Your Tasks** in the Streamlit app (http://localhost:8501)
2. **Export** using "Export for LLM Analysis" button
3. **Upload** the exported file to Bob
4. **Get Guidance** on optimal execution order

## File Formats

Bob IDE requires a specific YAML structure. We provide three files:

- **For Bob IDE**: Use `task-prioritizer-export.yaml` ⭐ (Bob IDE format with `customModes:` structure)
- **Alternative YAML**: `task-prioritizer.yaml` (Standard YAML, may not work with Bob IDE)
- **JSON Format**: `task-prioritizer.json` (For other tools or Bob versions)

**Always use `task-prioritizer-export.yaml` for Bob IDE!**

## Troubleshooting

### Mode Not Importing
- ⭐ Ensure you're using `task-prioritizer-export.yaml` (the one with `customModes:` structure)
- NOT `task-prioritizer.yaml` or `task-prioritizer.json`
- Check that Bob IDE is up to date
- Try restarting Bob IDE after import
- Verify the file has the correct structure (starts with `customModes:`)

### Mode Imported But Not Working
- Verify you've selected the mode (look for 📋 icon)
- Try the simple 3-task test first
- Check Bob IDE's console for any errors

## What's Next?

Once installed, the mode will:
- ✅ Analyze task dependencies
- ✅ Provide numbered execution steps
- ✅ Explain WHY each task comes in that order
- ✅ Identify risks and blockers
- ✅ Suggest parallel work opportunities
- ✅ Group tasks into sprints

For detailed usage instructions, see `bob-custom-modes/README.md`

---

**That's it!** You're ready to get AI-powered task prioritization guidance. 🚀