"""
Task analysis engine for dependency detection, prioritization, and execution planning.
"""
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict, deque
from models import Task, TaskCollection


class TaskAnalyzer:
    """Analyzes tasks for dependencies, execution order, and risks."""
    
    def __init__(self, task_collection: TaskCollection):
        self.task_collection = task_collection
        self.tasks = task_collection.tasks
        self.task_map = {task.id: task for task in self.tasks}
    
    def analyze_all(self) -> Dict[str, Any]:
        """
        Perform complete analysis of all tasks.
        
        Returns:
            Dictionary containing all analysis results
        """
        # Get execution order (list of dicts)
        execution_order_full = self.calculate_execution_order()
        execution_order_ids = [item['task_id'] for item in execution_order_full]
        
        # Get dependencies analysis
        dependencies_analysis = self.analyze_dependencies()
        
        # Add circular dependencies to dependencies dict
        circular = self._detect_circular_dependencies()
        dependencies_analysis['circular_dependencies'] = [circular] if circular else []
        
        return {
            'summary': self.get_summary(),
            'execution_order': execution_order_ids,
            'dependencies': dependencies_analysis,
            'risks': self.assess_risks(),
            'parallel_opportunities': self.find_parallel_opportunities(),
            'sprint_plan': self.generate_sprint_plan(),
            'technology_map': self.map_technologies()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        priority_counts = {'high': 0, 'medium': 0, 'low': 0}
        status_counts = {'pending': 0, 'in-progress': 0, 'completed': 0}
        total_effort = 0
        
        for task in self.tasks:
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
            status_counts[task.status] = status_counts.get(task.status, 0) + 1
            
            # Try to extract numeric effort
            if task.estimated_effort:
                try:
                    # Extract first number from effort string
                    import re
                    numbers = re.findall(r'\d+', task.estimated_effort)
                    if numbers:
                        total_effort += int(numbers[0])
                except:
                    pass
        
        return {
            'total_tasks': len(self.tasks),
            'priority_counts': priority_counts,
            'status_counts': status_counts,
            'estimated_timeline': f"{total_effort} days" if total_effort > 0 else "Not specified",
            'completion_rate': round(status_counts['completed'] / len(self.tasks) * 100, 1) if self.tasks else 0
        }
    
    def calculate_execution_order(self) -> List[Dict[str, Any]]:
        """
        Calculate optimal execution order using topological sort.
        
        Returns:
            List of tasks in execution order with metadata
        """
        # Build dependency graph
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        
        # Initialize all tasks
        for task in self.tasks:
            if task.id not in in_degree:
                in_degree[task.id] = 0
        
        # Build edges
        for task in self.tasks:
            for dep_id in task.dependencies:
                if dep_id in self.task_map:
                    graph[dep_id].append(task.id)
                    in_degree[task.id] += 1
        
        # Topological sort with priority consideration
        queue = deque()
        
        # Start with tasks that have no dependencies
        for task_id, degree in in_degree.items():
            if degree == 0:
                queue.append(task_id)
        
        execution_order = []
        step = 1
        
        while queue:
            # Sort current level by priority
            current_level = list(queue)
            queue.clear()
            
            # Sort by priority (high > medium > low)
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            current_level.sort(key=lambda tid: priority_order.get(self.task_map[tid].priority, 3))
            
            for task_id in current_level:
                task = self.task_map[task_id]
                
                # Get dependency names
                dep_names = []
                for dep_id in task.dependencies:
                    if dep_id in self.task_map:
                        dep_names.append(self.task_map[dep_id].title)
                
                # Get what this enables
                enables = []
                for next_id in graph[task_id]:
                    if next_id in self.task_map:
                        enables.append(self.task_map[next_id].title)
                
                execution_order.append({
                    'step': step,
                    'task_id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority,
                    'estimated_effort': task.estimated_effort,
                    'dependencies': dep_names,
                    'enables': enables,
                    'labels': task.labels,
                    'notes': task.notes
                })
                
                step += 1
                
                # Reduce in-degree for dependent tasks
                for next_id in graph[task_id]:
                    in_degree[next_id] -= 1
                    if in_degree[next_id] == 0:
                        queue.append(next_id)
        
        # Check for circular dependencies
        if len(execution_order) < len(self.tasks):
            # Some tasks couldn't be ordered - circular dependency
            remaining = set(self.task_map.keys()) - {item['task_id'] for item in execution_order}
            for task_id in remaining:
                task = self.task_map[task_id]
                execution_order.append({
                    'step': step,
                    'task_id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority,
                    'estimated_effort': task.estimated_effort,
                    'dependencies': [self.task_map[d].title for d in task.dependencies if d in self.task_map],
                    'enables': [],
                    'labels': task.labels,
                    'notes': task.notes,
                    'warning': 'Circular dependency detected'
                })
                step += 1
        
        return execution_order
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze dependency relationships."""
        issues = []
        
        # Check for circular dependencies
        circular = self._detect_circular_dependencies()
        if circular:
            issues.append({
                'type': 'circular_dependency',
                'severity': 'high',
                'message': f"Circular dependency detected: {' → '.join(circular)}"
            })
        
        # Check for missing dependencies
        for task in self.tasks:
            for dep_id in task.dependencies:
                if dep_id not in self.task_map:
                    issues.append({
                        'type': 'missing_dependency',
                        'severity': 'medium',
                        'task': task.title,
                        'message': f"Task '{task.title}' depends on non-existent task (ID: {dep_id[:8]}...)"
                    })
        
        # Calculate dependency depth
        max_depth = 0
        for task in self.tasks:
            depth = self._calculate_dependency_depth(task.id, set())
            max_depth = max(max_depth, depth)
        
        return {
            'issues': issues,
            'max_dependency_depth': max_depth,
            'total_dependencies': sum(len(task.dependencies) for task in self.tasks)
        }
    
    def assess_risks(self) -> List[Dict[str, Any]]:
        """Assess risks for each task."""
        risks = []
        
        for task in self.tasks:
            risk_level = 'low'
            risk_factors = []
            
            # High priority tasks are higher risk
            if task.priority == 'high':
                risk_factors.append('High priority - critical to project')
                risk_level = 'medium'
            
            # Tasks with many dependencies are risky
            if len(task.dependencies) >= 3:
                risk_factors.append(f'Multiple dependencies ({len(task.dependencies)})')
                risk_level = 'high' if risk_level == 'medium' else 'medium'
            
            # Tasks that many others depend on are risky
            dependents = sum(1 for t in self.tasks if task.id in t.dependencies)
            if dependents >= 3:
                risk_factors.append(f'Critical path - {dependents} tasks depend on this')
                risk_level = 'high'
            
            # Long effort estimates are risky
            if task.estimated_effort:
                try:
                    import re
                    numbers = re.findall(r'\d+', task.estimated_effort)
                    if numbers and int(numbers[0]) >= 5:
                        risk_factors.append('Long duration task')
                        risk_level = 'high' if risk_level == 'medium' else 'medium'
                except:
                    pass
            
            # Complex labels indicate risk
            complex_labels = ['integration', 'security', 'payment', 'authentication', 'migration']
            if any(label.lower() in complex_labels for label in task.labels):
                risk_factors.append('Complex technical requirements')
                risk_level = 'high' if risk_level == 'medium' else 'medium'
            
            if risk_factors:
                risks.append({
                    'task_id': task.id,
                    'task_title': task.title,
                    'risk_level': risk_level,
                    'risk_factors': risk_factors
                })
        
        # Sort by risk level
        risk_order = {'high': 0, 'medium': 1, 'low': 2}
        risks.sort(key=lambda r: risk_order[r['risk_level']])
        
        return risks
    
    def find_parallel_opportunities(self) -> List[List[str]]:
        """Find tasks that can be done in parallel. Returns list of task ID groups."""
        execution_order = self.calculate_execution_order()
        
        # Group tasks by their step/level
        parallel_groups = []
        current_group = []
        last_step = -1
        
        for item in execution_order:
            current_step = item.get('step', 0)
            
            if current_step == last_step:
                current_group.append(item['task_id'])
            else:
                if len(current_group) > 1:
                    parallel_groups.append(current_group)
                current_group = [item['task_id']]
                last_step = current_step
        
        # Add last group if it has multiple tasks
        if len(current_group) > 1:
            parallel_groups.append(current_group)
        
        return parallel_groups
    
    def generate_sprint_plan(self, sprint_duration: int = 10) -> List[Dict[str, Any]]:
        """Generate sprint plan based on execution order."""
        execution_order = self.calculate_execution_order()
        sprints = []
        current_sprint = []
        current_effort = 0
        sprint_num = 1
        
        for item in execution_order:
            effort = self._extract_effort(item['estimated_effort'])
            
            if current_effort + effort > sprint_duration and current_sprint:
                # Calculate priority mix
                priority_counts = {'high': 0, 'medium': 0, 'low': 0}
                for t in current_sprint:
                    priority_counts[t['priority']] = priority_counts.get(t['priority'], 0) + 1
                priority_mix = ', '.join([f"{count} {p}" for p, count in priority_counts.items() if count > 0])
                
                # Start new sprint
                sprints.append({
                    'sprint_number': sprint_num,
                    'tasks': [t['task_id'] for t in current_sprint],
                    'total_effort': f"{current_effort} story points",
                    'task_count': len(current_sprint),
                    'priority_mix': priority_mix
                })
                current_sprint = []
                current_effort = 0
                sprint_num += 1
            
            current_sprint.append(item)
            current_effort += effort
        
        # Add remaining tasks
        if current_sprint:
            # Calculate priority mix
            priority_counts = {'high': 0, 'medium': 0, 'low': 0}
            for t in current_sprint:
                priority_counts[t['priority']] = priority_counts.get(t['priority'], 0) + 1
            priority_mix = ', '.join([f"{count} {p}" for p, count in priority_counts.items() if count > 0])
            
            sprints.append({
                'sprint_number': sprint_num,
                'tasks': [t['task_id'] for t in current_sprint],
                'total_effort': f"{current_effort} story points",
                'task_count': len(current_sprint),
                'priority_mix': priority_mix
            })
        
        return sprints
    
    def map_technologies(self) -> Dict[str, List[str]]:
        """Map technologies/skills to tasks."""
        tech_map = defaultdict(list)
        
        for task in self.tasks:
            for label in task.labels:
                tech_map[label].append(task.title)
        
        return dict(tech_map)
    
    def _detect_circular_dependencies(self) -> List[str]:
        """Detect circular dependencies using DFS."""
        visited = set()
        rec_stack = set()
        
        def dfs(task_id: str, path: List[str]) -> List[str]:
            visited.add(task_id)
            rec_stack.add(task_id)
            path.append(self.task_map[task_id].title if task_id in self.task_map else task_id)
            
            if task_id in self.task_map:
                for dep_id in self.task_map[task_id].dependencies:
                    if dep_id not in visited:
                        result = dfs(dep_id, path.copy())
                        if result:
                            return result
                    elif dep_id in rec_stack:
                        # Circular dependency found
                        cycle_start = path.index(self.task_map[dep_id].title if dep_id in self.task_map else dep_id)
                        return path[cycle_start:] + [path[cycle_start]]
            
            rec_stack.remove(task_id)
            return []
        
        for task_id in self.task_map:
            if task_id not in visited:
                result = dfs(task_id, [])
                if result:
                    return result
        
        return []
    
    def _calculate_dependency_depth(self, task_id: str, visited: Set[str]) -> int:
        """Calculate maximum dependency depth for a task."""
        if task_id in visited or task_id not in self.task_map:
            return 0
        
        visited.add(task_id)
        task = self.task_map[task_id]
        
        if not task.dependencies:
            return 1
        
        max_depth = 0
        for dep_id in task.dependencies:
            depth = self._calculate_dependency_depth(dep_id, visited.copy())
            max_depth = max(max_depth, depth)
        
        return max_depth + 1
    
    def _extract_effort(self, effort_str: str) -> int:
        """Extract numeric effort from string."""
        if not effort_str:
            return 1
        
        try:
            import re
            numbers = re.findall(r'\d+', effort_str)
            return int(numbers[0]) if numbers else 1
        except:
            return 1

# Made with Bob
