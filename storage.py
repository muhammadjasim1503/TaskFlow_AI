"""
Storage module for persisting tasks to JSON files.
"""
import json
import os
from pathlib import Path
from typing import Optional
from models import TaskCollection


class TaskStorage:
    """Handles reading and writing tasks to JSON storage."""
    
    def __init__(self, data_dir: str = "data", filename: str = "tasks.json"):
        """Initialize storage with data directory and filename."""
        self.data_dir = Path(data_dir)
        self.filename = filename
        self.filepath = self.data_dir / self.filename
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)
    
    def save(self, task_collection: TaskCollection) -> bool:
        """Save task collection to JSON file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(task_collection.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def load(self) -> Optional[TaskCollection]:
        """Load task collection from JSON file."""
        if not self.filepath.exists():
            return TaskCollection()
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return TaskCollection.from_dict(data)
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return TaskCollection()
    
    def export_for_llm(self, task_collection: TaskCollection, output_path: Optional[str] = None) -> str:
        """
        Export tasks in a format optimized for LLM analysis.
        Returns the formatted text and optionally saves to file.
        """
        lines = []
        lines.append(f"PROJECT: {task_collection.project_name}")
        lines.append(f"TOTAL TASKS: {len(task_collection.tasks)}")
        lines.append(f"LAST UPDATED: {task_collection.last_updated}")
        lines.append("\n" + "="*80 + "\n")
        
        for idx, task in enumerate(task_collection.tasks, 1):
            lines.append(f"=== TASK {idx} ===")
            lines.append(f"ID: {task.id}")
            lines.append(f"Title: {task.title}")
            lines.append(f"Description: {task.description}")
            lines.append(f"Priority: {task.priority}")
            lines.append(f"Estimated Effort: {task.estimated_effort or 'Not specified'}")
            lines.append(f"Labels: {', '.join(task.labels) if task.labels else 'None'}")
            lines.append(f"Status: {task.status}")
            
            # Show dependency titles instead of IDs for better readability
            if task.dependencies:
                dep_titles = []
                for dep_id in task.dependencies:
                    dep_task = task_collection.get_task(dep_id)
                    if dep_task:
                        dep_titles.append(f"{dep_task.title} (ID: {dep_id})")
                    else:
                        dep_titles.append(f"Unknown task (ID: {dep_id})")
                lines.append(f"Dependencies: {', '.join(dep_titles)}")
            else:
                lines.append("Dependencies: None")
            
            if task.notes:
                lines.append(f"Notes: {task.notes}")
            
            lines.append(f"Created: {task.created_at}")
            lines.append(f"Updated: {task.updated_at}")
            lines.append("\n" + "-"*80 + "\n")
        
        lines.append("\n=== ANALYSIS REQUEST ===")
        lines.append("Please analyze these tasks and provide:")
        lines.append("1. Optimal execution order considering dependencies")
        lines.append("2. Identification of any missing or circular dependencies")
        lines.append("3. Risk assessment for each task")
        lines.append("4. Recommended grouping or sprint planning")
        lines.append("5. Estimated timeline based on effort estimates")
        
        formatted_text = "\n".join(lines)
        
        # Save to file if output path is provided
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_text)
            except Exception as e:
                print(f"Error saving LLM export: {e}")
        
        return formatted_text

# Made with Bob
