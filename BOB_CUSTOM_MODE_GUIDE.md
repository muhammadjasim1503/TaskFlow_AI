# Using Task Data with Bob Custom Mode

This guide explains how to use the exported task data with Bob's custom mode for AI-powered task analysis and prioritization.

## Overview

The Task Input & Storage System exports your tasks in a format optimized for LLM analysis. You can use this with Bob's custom mode to get intelligent insights about task ordering, dependencies, and project planning.

## Step-by-Step Guide

### 1. Export Your Tasks

1. Open the Task Input & Storage System (running at `http://localhost:8501`)
2. Add all your development tasks with details
3. In the sidebar, click **"Export for LLM Analysis"**
4. Download the `tasks_for_llm.txt` file

### 2. Review the Export Format

The exported file contains:
- Project metadata (name, task count, last updated)
- Detailed task information for each task:
  - ID, Title, Description
  - Priority, Status, Estimated Effort
  - Labels and Dependencies
  - Additional notes
  - Timestamps
- Pre-formatted analysis request prompts

### 3. Using with Bob Custom Mode

#### Option A: Direct Paste (Recommended for Small Projects)

1. Open the exported `tasks_for_llm.txt` file
2. Copy the entire content
3. In Bob, start a new conversation
4. Paste the content and ask Bob to analyze it

Example prompt:
```
[Paste the entire exported content here]

Based on these tasks, please provide your analysis.
```

#### Option B: File Upload (For Larger Projects)

1. In Bob, use the file attachment feature
2. Upload the `tasks_for_llm.txt` file
3. Ask Bob to analyze the tasks

Example prompt:
```
I've uploaded a file containing my development tasks. Please analyze them and provide recommendations.
```

### 4. What to Ask Bob

Here are effective prompts to get the most value:

#### Task Prioritization
```
Analyze these tasks and suggest the optimal execution order, considering:
1. Dependencies between tasks
2. Priority levels
3. Estimated effort
4. Risk factors
```

#### Dependency Analysis
```
Review the task dependencies and identify:
1. Any circular dependencies
2. Missing dependencies that should be added
3. Tasks that could be parallelized
4. Critical path tasks
```

#### Sprint Planning
```
Based on these tasks, create a sprint plan:
1. Group tasks into logical sprints
2. Estimate sprint duration
3. Identify potential blockers
4. Suggest team allocation if applicable
```

#### Risk Assessment
```
Analyze these tasks for risks:
1. High-complexity tasks that need more planning
2. Tasks with unclear requirements
3. Dependencies that could cause delays
4. Technical debt considerations
```

#### Timeline Estimation
```
Based on the effort estimates, provide:
1. Overall project timeline
2. Critical milestones
3. Buffer time recommendations
4. Resource allocation suggestions
```

## Creating a Bob Custom Mode (Future Enhancement)

### Custom Mode Configuration

You can create a dedicated Bob custom mode for task analysis. Here's a suggested configuration:

**Mode Name:** Task Analyzer

**System Prompt:**
```
You are an expert project manager and software architect specializing in task analysis and prioritization. 

When analyzing development tasks, you should:
1. Identify optimal execution order based on dependencies
2. Detect circular or missing dependencies
3. Assess complexity and risk for each task
4. Suggest sprint/milestone groupings
5. Provide timeline estimates
6. Recommend parallelization opportunities
7. Flag tasks needing more clarification

Always provide actionable, specific recommendations with clear reasoning.
```

**Tools/Capabilities:**
- Code analysis
- Dependency graph visualization
- Timeline estimation
- Risk assessment

### Using the Custom Mode

Once created, you can:
1. Upload your `tasks_for_llm.txt` file
2. The mode will automatically analyze using the specialized prompt
3. Get consistent, high-quality task analysis

## Example Analysis Output

When you provide your tasks to Bob, expect output like:

```
TASK ANALYSIS REPORT
====================

EXECUTION ORDER:
1. Task: Setup Database Schema (ID: abc123)
   Reason: Foundation for all data-related tasks
   Priority: HIGH
   
2. Task: Create API Endpoints (ID: def456)
   Reason: Depends on database, needed by frontend
   Priority: HIGH
   
3. Task: Build User Interface (ID: ghi789)
   Reason: Depends on API endpoints
   Priority: MEDIUM

DEPENDENCY ISSUES:
- Task "User Authentication" (ID: jkl012) should depend on "Setup Database Schema"
- Circular dependency detected: Task A → Task B → Task C → Task A

RISK ASSESSMENT:
- HIGH RISK: "Implement Payment Gateway" - Complex integration, needs security review
- MEDIUM RISK: "Real-time Notifications" - WebSocket complexity

SPRINT RECOMMENDATIONS:
Sprint 1 (2 weeks): Database setup, API foundation
Sprint 2 (2 weeks): Core API endpoints, authentication
Sprint 3 (2 weeks): Frontend development, UI components

TIMELINE ESTIMATE:
Total: 6-8 weeks
Critical Path: Database → API → Frontend (6 weeks minimum)
Buffer: 2 weeks for testing and refinement
```

## Tips for Best Results

1. **Be Detailed**: Provide comprehensive task descriptions
2. **Link Dependencies**: Explicitly mark task dependencies
3. **Use Labels**: Tag tasks with relevant categories
4. **Estimate Effort**: Include realistic effort estimates
5. **Add Context**: Use the notes field for important context
6. **Update Regularly**: Re-export and re-analyze as tasks evolve

## Iterative Analysis

You can iterate with Bob:

1. Get initial analysis
2. Update tasks based on recommendations
3. Re-export and re-analyze
4. Refine until you have an optimal plan

## Integration with Development Workflow

### Daily Standup
- Export tasks before standup
- Use Bob's analysis to guide discussion
- Update task status after standup

### Sprint Planning
- Export all backlog items
- Use Bob to group into sprints
- Assign based on recommendations

### Risk Review
- Weekly export and analysis
- Track risk trends over time
- Proactive issue identification

## Troubleshooting

### Bob doesn't understand the format
- Ensure you copied the entire export
- Check that the file isn't corrupted
- Try breaking into smaller chunks if too large

### Analysis is too generic
- Add more detail to task descriptions
- Include specific technical context
- Ask more specific questions

### Missing dependencies not detected
- Be explicit about technical relationships
- Add notes about implicit dependencies
- Ask Bob to review specific task pairs

## Future Enhancements

Planned features for better Bob integration:
- Direct API integration with Bob
- Automated analysis scheduling
- Custom mode templates
- Visual dependency graphs
- Historical analysis tracking

## Support

For issues or questions:
- Check the main README.md
- Review task export format
- Ensure all required fields are filled
- Try with sample data first

---

**Note:** This guide assumes you have access to Bob AI assistant. The analysis quality depends on the detail and accuracy of your task information.