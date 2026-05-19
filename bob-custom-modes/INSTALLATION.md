# Installing the Task Prioritizer Custom Mode for Bob

This guide walks you through installing and testing the Task Prioritizer custom mode for Bob AI Assistant.

## Prerequisites

- Bob AI Assistant installed and running
- Access to Bob's custom modes feature
- The `task-prioritizer.yaml` file from this project (YAML format required by Bob IDE)

## Installation Steps

### Step 1: Locate Bob's Custom Modes Directory

The location varies by operating system:

**Windows:**
```
%APPDATA%\Bob\custom-modes\
```
Full path example: `C:\Users\YourUsername\AppData\Roaming\Bob\custom-modes\`

**macOS:**
```
~/Library/Application Support/Bob/custom-modes/
```

**Linux:**
```
~/.config/Bob/custom-modes/
```

### Step 2: Create Directory (if needed)

If the `custom-modes` directory doesn't exist, create it:

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Bob\custom-modes"
```

**macOS/Linux:**
```bash
mkdir -p ~/Library/Application\ Support/Bob/custom-modes/
# or for Linux:
mkdir -p ~/.config/Bob/custom-modes/
```

### Step 3: Copy the Mode File

**Windows (PowerShell):**
```powershell
Copy-Item "bob-custom-modes\task-prioritizer.yaml" "$env:APPDATA\Bob\custom-modes\"
```

**macOS/Linux:**
```bash
cp bob-custom-modes/task-prioritizer.yaml ~/Library/Application\ Support/Bob/custom-modes/
# or for Linux:
cp bob-custom-modes/task-prioritizer.yaml ~/.config/Bob/custom-modes/
```

### Step 4: Restart Bob

1. Completely quit Bob (not just close the window)
2. Restart Bob
3. Wait for it to fully load

### Step 5: Verify Installation

1. Open Bob
2. Look for the mode selector (usually a dropdown at the top)
3. You should see "📋 Task Prioritizer" in the list
4. Select it to activate the mode

## Alternative Installation Method: Import via Bob IDE (Recommended)

**This is the easiest method for Bob IDE:**

1. Open Bob IDE
2. Look for the **Custom Modes** section or **Import Mode** option
3. Click **"Import Mode"** or **"+"** button
4. Navigate to `bob-custom-modes/task-prioritizer.yaml`
5. Select the YAML file and click **"Import"** or **"Open"**
6. Confirm the import
7. The mode should now appear in your mode selector as "📋 Task Prioritizer"

**Note:** Bob IDE requires YAML format (.yaml) for custom modes, not JSON.

## Testing the Installation

### Quick Test

1. **Switch to Task Prioritizer mode**
   - Select "📋 Task Prioritizer" from the mode dropdown

2. **Send a test message**
   ```
   I have 3 tasks:
   1. Setup database (no dependencies)
   2. Create API (depends on database)
   3. Build frontend (depends on API)
   
   What order should I do them in?
   ```

3. **Expected Response**
   You should get a structured response with:
   - Task analysis summary
   - Step-by-step execution plan
   - Clear reasoning for each step
   - Dependencies highlighted

### Full Test with Sample File

1. **Use the provided sample file**
   - File: `sample-tasks-for-testing.txt`
   - Contains 8 realistic e-commerce project tasks

2. **Upload to Bob**
   - Click the attachment icon in Bob
   - Select `sample-tasks-for-testing.txt`
   - Or copy/paste the entire content

3. **Ask for analysis**
   ```
   Please analyze these tasks and provide a step-by-step execution plan.
   ```

4. **Expected Response Format**
   ```
   📊 TASK ANALYSIS SUMMARY
   - Total tasks: 8
   - Dependencies identified
   - Critical path outlined
   - Timeline estimate
   
   ⚠️ ISSUES DETECTED
   [Any problems found]
   
   🎯 STEP-BY-STEP EXECUTION PLAN
   
   STEP 1: Setup PostgreSQL Database Schema
   ID: a1b2c3d4...
   Priority: HIGH
   Effort: 3 days
   
   WHY THIS STEP:
   Foundation for entire application...
   
   [Continues for all tasks]
   ```

## Troubleshooting

### Mode Not Appearing

**Problem:** Task Prioritizer doesn't show in mode selector

**Solutions:**
1. Verify file is in correct directory
2. Check file name is exactly `task-prioritizer.json`
3. Validate JSON syntax (use a JSON validator)
4. Restart Bob completely (quit and reopen)
5. Check Bob's logs for errors

**Check YAML Syntax:**
```bash
# On systems with Python
python -c "import yaml; yaml.safe_load(open('bob-custom-modes/task-prioritizer.yaml'))"

# Or use online validator: yamllint.com
```

### Mode Appears But Doesn't Work

**Problem:** Mode is visible but responses are generic

**Solutions:**
1. Verify you've actually selected the mode (check for 📋 icon)
2. Try a simple test query first
3. Check if Bob has internet connection (if required)
4. Review Bob's settings for custom mode permissions

### File Permission Issues

**Problem:** Can't copy file to custom modes directory

**Solutions:**

**Windows:**
```powershell
# Run PowerShell as Administrator
Start-Process powershell -Verb runAs
# Then copy the file
```

**macOS/Linux:**
```bash
# Check permissions
ls -la ~/Library/Application\ Support/Bob/custom-modes/

# Fix permissions if needed
chmod 755 ~/Library/Application\ Support/Bob/custom-modes/
chmod 644 ~/Library/Application\ Support/Bob/custom-modes/task-prioritizer.json
```

### YAML Validation Errors

**Problem:** Bob reports YAML syntax error

**Solution:**
1. Open `task-prioritizer.yaml` in a text editor
2. Check for:
   - Incorrect indentation (YAML is indent-sensitive)
   - Missing colons
   - Invalid characters
3. Use a YAML validator to find the exact error
4. Fix and re-copy the file

## Verifying Mode Configuration

After installation, verify the mode settings:

1. **Check Mode Name:** Should be "Task Prioritizer"
2. **Check Icon:** Should be 📋
3. **Check Slug:** Should be "task-prioritizer"
4. **Check Capabilities:**
   - File access: Enabled
   - Code execution: Disabled
   - Web search: Disabled

## Updating the Mode

To update the mode after changes:

1. Edit `task-prioritizer.yaml` in your project
2. Copy the updated file to Bob's directory (overwrite existing)
3. Restart Bob
4. Changes should take effect

## Uninstalling

To remove the mode:

1. Navigate to Bob's custom modes directory
2. Delete `task-prioritizer.yaml`
3. Restart Bob
4. Mode will no longer appear in selector

## Getting Help

If you encounter issues:

1. **Check Bob's Documentation**
   - Look for custom modes section
   - Review troubleshooting guides

2. **Verify File Integrity**
   - Ensure JSON is valid
   - Check file isn't corrupted

3. **Test with Simple Example**
   - Use the quick test above
   - Verify basic functionality

4. **Review Logs**
   - Check Bob's error logs
   - Look for custom mode loading errors

## Next Steps

After successful installation:

1. Read `bob-custom-modes/README.md` for usage guide
2. Try the sample tasks file
3. Export your own tasks from the Streamlit app
4. Start using Task Prioritizer for your projects!

## Advanced Configuration

### Customizing the Mode

You can edit `task-prioritizer.json` to customize:

**Change Temperature:**
```json
"temperature": 0.7  // 0.0 = deterministic, 1.0 = creative
```

**Modify System Prompt:**
Edit the `systemPrompt` field to adjust behavior

**Add Custom Shortcuts:**
Add entries to the `shortcuts` array

**After Changes:**
1. Save the file
2. Copy to Bob's directory
3. Restart Bob

### Creating Variations

You can create multiple versions:

1. Copy `task-prioritizer.yaml`
2. Rename (e.g., `task-prioritizer-agile.yaml`)
3. Change `slug` and `name` fields
4. Modify system prompt for different approach
5. Install both versions

## System Requirements

- **Bob Version:** Any version with custom mode support
- **Disk Space:** < 1 MB
- **Permissions:** Read access to custom modes directory

## Security Notes

- The mode only has file read access
- No code execution capabilities
- No web search or external API calls
- Safe to use with sensitive project data

---

**Installation Complete!** 🎉

You're now ready to use the Task Prioritizer mode. Start by testing with the sample file, then export your own tasks from the Streamlit app.

For usage instructions, see `bob-custom-modes/README.md`