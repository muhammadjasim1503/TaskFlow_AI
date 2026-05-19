"""
Task Input & Storage System - Streamlit Application
Collects developer tasks and saves them in LLM-friendly format.
Enhanced with AI-powered file parsing and analysis.
"""
import streamlit as st
from models import Task, TaskCollection
from storage import TaskStorage
from ai_parser import TaskParser
from analyzer import TaskAnalyzer
from visualizations import (
    create_dependency_graph,
    create_timeline_gantt,
    create_risk_chart,
    create_sprint_timeline
)
import json


# Initialize storage
storage = TaskStorage()

# Page configuration
st.set_page_config(
    page_title="Task Input System",
    page_icon="📋",
    layout="wide"
)

# Initialize session state
if 'task_collection' not in st.session_state:
    loaded_collection = storage.load()
    st.session_state.task_collection = loaded_collection if loaded_collection else TaskCollection()
if 'editing_task_id' not in st.session_state:
    st.session_state.editing_task_id = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'parsed_tasks' not in st.session_state:
    st.session_state.parsed_tasks = []


def save_tasks():
    """Save tasks to storage."""
    storage.save(st.session_state.task_collection)


def add_task(task: Task):
    """Add a new task."""
    st.session_state.task_collection.add_task(task)
    save_tasks()


def delete_task(task_id: str):
    """Delete a task."""
    st.session_state.task_collection.remove_task(task_id)
    save_tasks()


def update_task(task_id: str, updated_task: Task):
    """Update an existing task."""
    st.session_state.task_collection.update_task(task_id, updated_task)
    save_tasks()


def get_task_options():
    """Get list of tasks for dependency selection."""
    return {f"{task.title} (ID: {task.id[:8]}...)": task.id 
            for task in st.session_state.task_collection.tasks}


# Main UI
st.title("📋 Task Input & Storage System")
st.markdown("Collect and organize development tasks for LLM analysis")

# Sidebar for project settings
with st.sidebar:
    st.header("⚙️ Project Settings")
    project_name = st.text_input(
        "Project Name",
        value=st.session_state.task_collection.project_name
    )
    if project_name != st.session_state.task_collection.project_name:
        st.session_state.task_collection.project_name = project_name
        save_tasks()
    
    st.divider()
    st.metric("Total Tasks", len(st.session_state.task_collection.tasks))
    
    st.divider()
    st.subheader("📤 Export Options")
    
    if st.button("Export for LLM Analysis", use_container_width=True):
        llm_text = storage.export_for_llm(st.session_state.task_collection)
        st.download_button(
            label="Download LLM Export",
            data=llm_text,
            file_name="tasks_for_llm.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    if st.button("Export as JSON", use_container_width=True):
        import json
        json_data = json.dumps(
            st.session_state.task_collection.to_dict(),
            indent=2,
            ensure_ascii=False
        )
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="tasks.json",
            mime="application/json",
            use_container_width=True
        )

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload & Parse",
    "➕ Manual Entry",
    "📋 Task List",
    "📊 Analysis Results"
])

with tab1:
    st.header("Upload & Parse Tasks with AI")
    st.markdown("Upload your tasks in any format and let AI parse them automatically!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['txt', 'csv', 'json', 'xlsx', 'xls', 'md'],
        help="Supported formats: Text, CSV, JSON, Excel, Markdown"
    )
    
    if uploaded_file:
        st.info(f"📄 File uploaded: {uploaded_file.name}")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🤖 Parse with AI", type="primary", use_container_width=True):
                with st.spinner("Parsing tasks with AI... This may take a moment."):
                    try:
                        # Read file content
                        file_content = uploaded_file.read()
                        
                        # Initialize parser
                        parser = TaskParser()
                        
                        # Parse based on file type
                        file_extension = uploaded_file.name.split('.')[-1].lower()
                        parsed_tasks = parser.parse_file(file_content, file_extension)
                        
                        if parsed_tasks:
                            st.session_state.parsed_tasks = parsed_tasks
                            st.success(f"✅ Successfully parsed {len(parsed_tasks)} tasks!")
                        else:
                            st.error("❌ No tasks could be parsed from the file.")
                    except Exception as e:
                        st.error(f"❌ Error parsing file: {str(e)}")
        
        # Display parsed tasks
        if st.session_state.parsed_tasks:
            st.divider()
            st.subheader("Parsed Tasks Preview")
            
            for i, task_data in enumerate(st.session_state.parsed_tasks):
                with st.expander(f"Task {i+1}: {task_data.get('title', 'Untitled')}", expanded=i==0):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {task_data.get('description', 'N/A')}")
                        st.markdown(f"**Priority:** {task_data.get('priority', 'medium')}")
                        st.markdown(f"**Status:** {task_data.get('status', 'pending')}")
                        
                        if task_data.get('labels'):
                            st.markdown(f"**Labels:** {', '.join(task_data['labels'])}")
                        if task_data.get('estimated_effort'):
                            st.markdown(f"**Effort:** {task_data['estimated_effort']}")
                        if task_data.get('dependencies'):
                            st.markdown(f"**Dependencies:** {', '.join(task_data['dependencies'])}")
                    
                    with col2:
                        st.json(task_data)
            
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Add All to Task List", type="primary", use_container_width=True):
                    added_count = 0
                    for task_data in st.session_state.parsed_tasks:
                        try:
                            new_task = Task(
                                title=task_data.get('title', 'Untitled'),
                                description=task_data.get('description', ''),
                                priority=task_data.get('priority', 'medium'),
                                status=task_data.get('status', 'pending'),
                                estimated_effort=task_data.get('estimated_effort', ''),
                                labels=task_data.get('labels', []),
                                dependencies=task_data.get('dependencies', []),
                                notes=task_data.get('notes', '')
                            )
                            add_task(new_task)
                            added_count += 1
                        except Exception as e:
                            st.error(f"Error adding task: {str(e)}")
                    
                    if added_count > 0:
                        st.success(f"✅ Added {added_count} tasks to the collection!")
                        st.session_state.parsed_tasks = []
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Clear Parsed Tasks", use_container_width=True):
                    st.session_state.parsed_tasks = []
                    st.rerun()

with tab2:
    st.header("Task Input Form")
    
    # Check if we're editing
    editing_task = None
    if st.session_state.editing_task_id:
        editing_task = st.session_state.task_collection.get_task(
            st.session_state.editing_task_id
        )
    
    with st.form("task_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            title = st.text_input(
                "Task Title *",
                value=editing_task.title if editing_task else "",
                placeholder="e.g., Implement user authentication"
            )
            
            description = st.text_area(
                "Description *",
                value=editing_task.description if editing_task else "",
                placeholder="Detailed description of the task...",
                height=150
            )
        
        with col2:
            priority = st.selectbox(
                "Priority",
                options=["high", "medium", "low"],
                index=["high", "medium", "low"].index(
                    editing_task.priority if editing_task else "medium"
                )
            )
            
            status = st.selectbox(
                "Status",
                options=["pending", "in-progress", "completed"],
                index=["pending", "in-progress", "completed"].index(
                    editing_task.status if editing_task else "pending"
                )
            )
            
            estimated_effort = st.text_input(
                "Estimated Effort",
                value=editing_task.estimated_effort if editing_task else "",
                placeholder="e.g., 2 hours, 3 story points"
            )
        
        # Labels input
        labels_input = st.text_input(
            "Labels (comma-separated)",
            value=", ".join(editing_task.labels) if editing_task else "",
            placeholder="e.g., frontend, backend, bug, feature"
        )
        
        # Dependencies selection
        task_options = get_task_options()
        if editing_task:
            # Remove current task from options when editing
            task_options = {k: v for k, v in task_options.items() 
                          if v != editing_task.id}
        
        selected_deps = st.multiselect(
            "Dependencies (select prerequisite tasks)",
            options=list(task_options.keys()),
            default=[k for k, v in task_options.items() 
                    if editing_task and v in editing_task.dependencies]
        )
        
        # Notes
        notes = st.text_area(
            "Additional Notes",
            value=editing_task.notes if editing_task else "",
            placeholder="Any additional context or information...",
            height=100
        )
        
        # Form buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            submit = st.form_submit_button(
                "Update Task" if editing_task else "Add Task",
                use_container_width=True,
                type="primary"
            )
        with col2:
            if editing_task:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
                if cancel:
                    st.session_state.editing_task_id = None
                    st.rerun()
        
        if submit:
            if not title or not description:
                st.error("Title and Description are required!")
            else:
                # Parse labels
                labels = [l.strip() for l in labels_input.split(",") if l.strip()]
                
                # Get dependency IDs
                dependencies = [task_options[k] for k in selected_deps]
                
                if editing_task:
                    # Update existing task
                    updated_task = Task(
                        id=editing_task.id,
                        title=title,
                        description=description,
                        priority=priority,
                        status=status,
                        estimated_effort=estimated_effort,
                        labels=labels,
                        dependencies=dependencies,
                        notes=notes,
                        created_at=editing_task.created_at,
                        updated_at=editing_task.updated_at
                    )
                    update_task(editing_task.id, updated_task)
                    st.success(f"✅ Task '{title}' updated successfully!")
                    st.session_state.editing_task_id = None
                else:
                    # Create new task
                    new_task = Task(
                        title=title,
                        description=description,
                        priority=priority,
                        status=status,
                        estimated_effort=estimated_effort,
                        labels=labels,
                        dependencies=dependencies,
                        notes=notes
                    )
                    add_task(new_task)
                    st.success(f"✅ Task '{title}' added successfully!")
                
                st.rerun()

with tab3:
    st.header("Task List")
    
    if not st.session_state.task_collection.tasks:
        st.info("No tasks yet. Add your first task in the 'Add/Edit Task' tab!")
    else:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_priority = st.multiselect(
                "Filter by Priority",
                options=["high", "medium", "low"],
                default=["high", "medium", "low"]
            )
        with col2:
            filter_status = st.multiselect(
                "Filter by Status",
                options=["pending", "in-progress", "completed"],
                default=["pending", "in-progress", "completed"]
            )
        with col3:
            search_term = st.text_input("Search", placeholder="Search tasks...")
        
        # Filter tasks
        filtered_tasks = [
            task for task in st.session_state.task_collection.tasks
            if task.priority in filter_priority
            and task.status in filter_status
            and (not search_term or 
                 search_term.lower() in task.title.lower() or
                 search_term.lower() in task.description.lower())
        ]
        
        st.markdown(f"**Showing {len(filtered_tasks)} of {len(st.session_state.task_collection.tasks)} tasks**")
        
        # Display tasks
        for task in filtered_tasks:
            with st.expander(f"**{task.title}** | {task.priority.upper()} | {task.status}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Description:** {task.description}")
                    
                    if task.labels:
                        st.markdown(f"**Labels:** {', '.join(task.labels)}")
                    
                    if task.estimated_effort:
                        st.markdown(f"**Estimated Effort:** {task.estimated_effort}")
                    
                    if task.dependencies:
                        dep_titles = []
                        for dep_id in task.dependencies:
                            dep_task = st.session_state.task_collection.get_task(dep_id)
                            if dep_task:
                                dep_titles.append(dep_task.title)
                        if dep_titles:
                            st.markdown(f"**Dependencies:** {', '.join(dep_titles)}")
                    
                    if task.notes:
                        st.markdown(f"**Notes:** {task.notes}")
                    
                    st.caption(f"ID: {task.id} | Created: {task.created_at[:10]}")
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{task.id}", use_container_width=True):
                        st.session_state.editing_task_id = task.id
                        st.rerun()
                    
                    if st.button("🗑️ Delete", key=f"delete_{task.id}", use_container_width=True):
                        delete_task(task.id)
                        st.rerun()
with tab4:
    st.header("📊 Analysis Results")
    
    if not st.session_state.task_collection.tasks:
        st.info("No tasks to analyze. Add tasks first!")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Total Tasks:** {len(st.session_state.task_collection.tasks)}")
        with col2:
            if st.button("🔄 Run Analysis", type="primary", use_container_width=True):
                with st.spinner("Analyzing tasks..."):
                    try:
                        # Create analyzer with TaskCollection
                        analyzer = TaskAnalyzer(st.session_state.task_collection)
                        
                        # Run complete analysis
                        analysis_results = analyzer.analyze_all()
                        
                        # Store results
                        st.session_state.analysis_results = analysis_results
                        
                        st.success("✅ Analysis complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Analysis error: {str(e)}")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Convert tasks to dict format for visualizations
            tasks_dict = [task.to_dict() for task in st.session_state.task_collection.tasks]
            
            # Create sub-tabs for different visualizations
            viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
                "📊 Summary",
                "🔗 Dependencies",
                "⚠️ Risk Assessment",
                "🏃 Sprint Planning"
            ])
            
            with viz_tab1:
                st.subheader("Project Summary")
                
                summary = results.get('summary', {})
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Tasks", summary.get('total_tasks', 0))
                with col2:
                    st.metric("High Priority", summary.get('priority_counts', {}).get('high', 0))
                with col3:
                    st.metric("In Progress", summary.get('status_counts', {}).get('in-progress', 0))
                with col4:
                    st.metric("Completed", summary.get('status_counts', {}).get('completed', 0))
                
                st.divider()
                
                # Priority distribution
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Priority Distribution**")
                    priority_counts = summary.get('priority_counts', {})
                    for priority, count in priority_counts.items():
                        st.markdown(f"- {priority.capitalize()}: {count}")
                
                with col2:
                    st.markdown("**Status Distribution**")
                    status_counts = summary.get('status_counts', {})
                    for status, count in status_counts.items():
                        st.markdown(f"- {status.capitalize()}: {count}")
            
            with viz_tab2:
                st.subheader("Task Dependencies")
                
                dependencies_info = results.get('dependencies', {})
                
                # Check for circular dependencies
                circular_deps = dependencies_info.get('circular_dependencies', [])
                if circular_deps:
                    st.error("⚠️ **Circular Dependencies Detected!**")
                    for cycle in circular_deps:
                        st.warning(f"Cycle: {' → '.join(cycle)}")
                else:
                    st.success("✅ No circular dependencies found")
                
                # Show dependency graph
                try:
                    fig = create_dependency_graph(tasks_dict)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating dependency graph: {str(e)}")
                
                # Show execution order
                st.divider()
                st.subheader("Recommended Execution Order")
                execution_order = results.get('execution_order', [])
                if execution_order:
                    for i, task_id in enumerate(execution_order, 1):
                        task = st.session_state.task_collection.get_task(task_id)
                        if task:
                            st.markdown(f"{i}. **{task.title}** ({task.priority} priority)")
                else:
                    st.info("Unable to determine execution order")
                
                # Show parallel opportunities
                st.divider()
                st.subheader("Parallel Execution Opportunities")
                parallel_opps = results.get('parallel_opportunities', [])
                if parallel_opps:
                    for group_num, group in enumerate(parallel_opps, 1):
                        with st.expander(f"Parallel Group {group_num} ({len(group)} tasks)"):
                            for task_id in group:
                                task = st.session_state.task_collection.get_task(task_id)
                                if task:
                                    st.markdown(f"- {task.title}")
                else:
                    st.info("No parallel execution opportunities identified")
            
            with viz_tab3:
                st.subheader("Risk Assessment")
                
                risks = results.get('risks', [])
                
                if risks:
                    try:
                        fig = create_risk_chart(risks)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating risk chart: {str(e)}")
                    
                    # Detailed risk breakdown
                    st.divider()
                    st.subheader("Detailed Risk Analysis")
                    
                    # Sort by risk level (high > medium > low)
                    risk_order = {'high': 0, 'medium': 1, 'low': 2}
                    sorted_risks = sorted(risks, key=lambda x: risk_order.get(x.get('risk_level', 'low'), 3))
                    
                    for risk_data in sorted_risks:
                        task_id = risk_data.get('task_id')
                        task = st.session_state.task_collection.get_task(task_id)
                        if task:
                            risk_level = risk_data.get('risk_level', 'low')
                            risk_icon = "🔴" if risk_level == 'high' else "🟡" if risk_level == 'medium' else "🟢"
                            
                            with st.expander(f"{risk_icon} {task.title} - {risk_level.upper()} Risk"):
                                st.markdown(f"**Task:** {task.title}")
                                st.markdown(f"**Priority:** {task.priority}")
                                st.markdown(f"**Status:** {task.status}")
                                
                                if risk_data.get('risk_factors'):
                                    st.markdown("**Risk Factors:**")
                                    for factor in risk_data['risk_factors']:
                                        st.markdown(f"- {factor}")
                else:
                    st.info("No significant risks identified")
            
            with viz_tab4:
                st.subheader("Sprint Planning Recommendation")
                
                sprint_plan = results.get('sprint_plan', [])
                
                if sprint_plan:
                    try:
                        fig = create_sprint_timeline(sprint_plan)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating sprint timeline: {str(e)}")
                    
                    st.divider()
                    
                    # Sprint breakdown
                    for sprint_num, sprint_data in enumerate(sprint_plan, 1):
                        tasks_in_sprint = sprint_data.get('tasks', [])
                        with st.expander(f"Sprint {sprint_num} ({len(tasks_in_sprint)} tasks)", expanded=sprint_num==1):
                            st.markdown(f"**Estimated Effort:** {sprint_data.get('total_effort', 'N/A')}")
                            st.markdown(f"**Priority Mix:** {sprint_data.get('priority_mix', 'N/A')}")
                            
                            st.markdown("**Tasks:**")
                            for task_id in tasks_in_sprint:
                                task = st.session_state.task_collection.get_task(task_id)
                                if task:
                                    effort = task.estimated_effort or "Not estimated"
                                    st.markdown(f"- **{task.title}** ({task.priority} priority, {effort})")
                else:
                    st.info("No sprint plan generated")
                
                # Technology map
                st.divider()
                st.subheader("Technology & Skill Dependencies")
                tech_map = results.get('technology_map', {})
                if tech_map:
                    for tech, task_ids in tech_map.items():
                        with st.expander(f"🔧 {tech} ({len(task_ids)} tasks)"):
                            for task_id in task_ids:
                                task = st.session_state.task_collection.get_task(task_id)
                                if task:
                                    st.markdown(f"- {task.title}")
                else:
                    st.info("No technology dependencies identified")
            
            # Export analysis results
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Export Analysis Report", use_container_width=True):
                    report = {
                        'project_name': st.session_state.task_collection.project_name,
                        'total_tasks': len(st.session_state.task_collection.tasks),
                        'analysis_results': results
                    }
                    report_json = json.dumps(report, indent=2, default=str)
                    st.download_button(
                        label="Download JSON Report",
                        data=report_json,
                        file_name="task_analysis_report.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            with col2:
                if st.button("🗑️ Clear Analysis", use_container_width=True):
                    st.session_state.analysis_results = None
                    st.rerun()


# Footer
st.divider()
st.caption("Task Input & Storage System | AI-Powered Analysis | Optimized for LLM")
