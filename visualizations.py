"""
Visualization components for task analysis using Plotly.
"""
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from typing import List, Dict, Any


def create_dependency_graph(tasks: List[Dict[str, Any]]) -> go.Figure:
    """
    Create an interactive dependency graph using Plotly and NetworkX.
    
    Args:
        tasks: List of task dictionaries with dependencies
        
    Returns:
        Plotly figure object
    """
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes
    task_map = {}
    for task in tasks:
        task_id = task.get('id', task.get('task_id', ''))
        task_title = task.get('title', 'Untitled')
        priority = task.get('priority', 'medium')
        
        G.add_node(task_id, title=task_title, priority=priority)
        task_map[task_id] = task_title
    
    # Add edges
    for task in tasks:
        task_id = task.get('id', task.get('task_id', ''))
        dependencies = task.get('dependencies', [])
        
        for dep_id in dependencies:
            if dep_id in task_map:
                G.add_edge(dep_id, task_id)
    
    # Use hierarchical layout
    try:
        pos = nx.spring_layout(G, k=2, iterations=50)
    except:
        pos = nx.random_layout(G)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines',
        showlegend=False
    )
    
    # Create node traces by priority
    priority_colors = {
        'high': '#ff6b6b',
        'medium': '#ffd93d',
        'low': '#6bcf7f'
    }
    
    node_traces = []
    
    for priority, color in priority_colors.items():
        node_x = []
        node_y = []
        node_text = []
        
        for node in G.nodes():
            if G.nodes[node].get('priority') == priority:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(G.nodes[node]['title'])
        
        if node_x:  # Only create trace if there are nodes with this priority
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=node_text,
                textposition="top center",
                name=f'{priority.capitalize()} Priority',
                marker=dict(
                    size=20,
                    color=color,
                    line=dict(width=2, color='white')
                )
            )
            node_traces.append(node_trace)
    
    # Create figure
    fig = go.Figure(data=[edge_trace] + node_traces)
    
    fig.update_layout(
        title=dict(text='Task Dependency Graph', font=dict(size=16)),
        showlegend=True,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        height=600
    )
    
    return fig


def create_priority_distribution(tasks: List[Dict[str, Any]]) -> go.Figure:
    """Create a pie chart showing priority distribution."""
    priority_counts = {'High': 0, 'Medium': 0, 'Low': 0}
    
    for task in tasks:
        priority = task.get('priority', 'medium').capitalize()
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    fig = go.Figure(data=[go.Pie(
        labels=list(priority_counts.keys()),
        values=list(priority_counts.values()),
        marker=dict(colors=['#ff6b6b', '#ffd93d', '#6bcf7f']),
        hole=0.3
    )])
    
    fig.update_layout(
        title='Task Priority Distribution',
        height=300
    )
    
    return fig


def create_timeline_gantt(execution_order: List[Dict[str, Any]]) -> go.Figure:
    """Create a Gantt-style timeline of task execution."""
    # Prepare data for Gantt chart
    tasks_data = []
    current_day = 0
    
    for item in execution_order:
        effort = _extract_effort(item.get('estimated_effort', '1'))
        
        tasks_data.append({
            'Task': item['title'][:30] + '...' if len(item['title']) > 30 else item['title'],
            'Start': current_day,
            'Finish': current_day + effort,
            'Priority': item.get('priority', 'medium').capitalize()
        })
        
        current_day += effort
    
    # Create figure
    fig = go.Figure()
    
    priority_colors = {
        'High': '#ff6b6b',
        'Medium': '#ffd93d',
        'Low': '#6bcf7f'
    }
    
    for i, task in enumerate(tasks_data):
        fig.add_trace(go.Bar(
            y=[task['Task']],
            x=[task['Finish'] - task['Start']],
            base=task['Start'],
            orientation='h',
            name=task['Priority'],
            marker=dict(color=priority_colors.get(task['Priority'], '#cccccc')),
            showlegend=i == 0 or task['Priority'] != tasks_data[i-1]['Priority'],
            hovertemplate=f"<b>{task['Task']}</b><br>Days {task['Start']}-{task['Finish']}<br>Duration: {task['Finish']-task['Start']} days<extra></extra>"
        ))
    
    fig.update_layout(
        title='Task Execution Timeline',
        xaxis_title='Days',
        yaxis_title='Tasks',
        barmode='stack',
        height=max(400, len(tasks_data) * 30),
        showlegend=True,
        hovermode='closest'
    )
    
    return fig


def create_technology_heatmap(tech_map: Dict[str, List[str]]) -> go.Figure:
    """Create a heatmap showing technology/skill distribution."""
    if not tech_map:
        # Return empty figure
        fig = go.Figure()
        fig.add_annotation(
            text="No technology labels found",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Prepare data
    technologies = list(tech_map.keys())
    task_counts = [len(tasks) for tasks in tech_map.values()]
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=technologies,
            y=task_counts,
            marker=dict(
                color=task_counts,
                colorscale='Viridis',
                showscale=True
            ),
            text=task_counts,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Technology/Skill Distribution',
        xaxis_title='Technology/Skill',
        yaxis_title='Number of Tasks',
        height=400
    )
    
    return fig


def create_risk_chart(risks: List[Dict[str, Any]]) -> go.Figure:
    """Create a chart showing risk assessment."""
    if not risks:
        fig = go.Figure()
        fig.add_annotation(
            text="No risks identified",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='green')
        )
        return fig
    
    # Count risks by level
    risk_counts = {'high': 0, 'medium': 0, 'low': 0}
    for risk in risks:
        level = risk.get('risk_level', 'low')
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=['High Risk', 'Medium Risk', 'Low Risk'],
            y=[risk_counts['high'], risk_counts['medium'], risk_counts['low']],
            marker=dict(color=['#ff6b6b', '#ffd93d', '#6bcf7f']),
            text=[risk_counts['high'], risk_counts['medium'], risk_counts['low']],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Risk Assessment Overview',
        yaxis_title='Number of Tasks',
        height=300
    )
    
    return fig


def create_sprint_timeline(sprints: List[Dict[str, Any]]) -> go.Figure:
    """Create a timeline showing sprint breakdown."""
    if not sprints:
        fig = go.Figure()
        fig.add_annotation(
            text="No sprints planned",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    sprint_numbers = [f"Sprint {s['sprint_number']}" for s in sprints]
    task_counts = [s['task_count'] for s in sprints]
    # Extract numeric effort from string
    efforts = [_extract_effort(str(s['total_effort'])) for s in sprints]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Task Count',
        x=sprint_numbers,
        y=task_counts,
        marker=dict(color='#4ecdc4'),
        text=task_counts,
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='Total Effort (days)',
        x=sprint_numbers,
        y=efforts,
        marker=dict(color='#ff6b6b'),
        text=efforts,
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Sprint Planning Overview',
        xaxis_title='Sprint',
        yaxis_title='Count',
        barmode='group',
        height=400
    )
    
    return fig


def _extract_effort(effort_str: str) -> int:
    """Extract numeric effort from string."""
    if not effort_str:
        return 1
    
    try:
        import re
        numbers = re.findall(r'\d+', str(effort_str))
        return int(numbers[0]) if numbers else 1
    except:
        return 1

# Made with Bob
