"""
Data models for task management system.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class Task:
    """Represents a development task with all necessary metadata for LLM analysis."""
    
    title: str
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    dependencies: List[str] = field(default_factory=list)
    priority: str = "medium"  # high, medium, low
    estimated_effort: str = ""  # e.g., "2 hours", "3 story points"
    labels: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, in-progress, completed
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self):
        """Convert task to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create task from dictionary."""
        return cls(**data)
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow().isoformat()


@dataclass
class TaskCollection:
    """Collection of tasks with metadata."""
    
    tasks: List[Task] = field(default_factory=list)
    project_name: str = "My Project"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def add_task(self, task: Task):
        """Add a task to the collection."""
        self.tasks.append(task)
        self.update_timestamp()
    
    def remove_task(self, task_id: str):
        """Remove a task by ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.update_timestamp()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: str, updated_task: Task):
        """Update a task by ID."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                updated_task.update_timestamp()
                self.tasks[i] = updated_task
                self.update_timestamp()
                return True
        return False
    
    def update_timestamp(self):
        """Update the last_updated timestamp."""
        self.last_updated = datetime.utcnow().isoformat()
    
    def to_dict(self):
        """Convert collection to dictionary."""
        return {
            "project_name": self.project_name,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "tasks": [task.to_dict() for task in self.tasks]
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create collection from dictionary."""
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(
            tasks=tasks,
            project_name=data.get("project_name", "My Project"),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            last_updated=data.get("last_updated", datetime.utcnow().isoformat())
        )

# Made with Bob
