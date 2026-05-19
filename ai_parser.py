"""
AI-powered task parser using Ollama.
Parses uploaded files in various formats and extracts structured task data.
"""
import json
import csv
import io
import requests
from typing import List, Dict, Any, Optional
import pandas as pd


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:7b"):
        self.base_url = base_url
        self.model = model
    
    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate text using Ollama."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            if system:
                payload["system"] = system
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama. Make sure Ollama is running (ollama serve)")
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")


class TaskParser:
    """Parse various file formats and extract task information using AI."""
    
    def __init__(self, ollama_model: str = "qwen2.5:7b"):
        self.ollama = OllamaClient(model=ollama_model)
    
    def parse_file(self, file_content: bytes, file_name: str) -> List[Dict[str, Any]]:
        """
        Parse uploaded file and extract tasks.
        
        Args:
            file_content: Raw file content as bytes
            file_name: Name of the uploaded file
            
        Returns:
            List of task dictionaries
        """
        file_ext = file_name.lower().split('.')[-1]
        
        # Convert to text based on file type
        if file_ext in ['txt', 'md']:
            text = file_content.decode('utf-8')
            return self.parse_text(text)
        
        elif file_ext == 'json':
            return self.parse_json(file_content)
        
        elif file_ext == 'csv':
            return self.parse_csv(file_content)
        
        elif file_ext in ['xlsx', 'xls']:
            return self.parse_excel(file_content)
        
        else:
            # Try to decode as text
            try:
                text = file_content.decode('utf-8')
                return self.parse_text(text)
            except:
                raise ValueError(f"Unsupported file format: {file_ext}")
    
    def parse_text(self, text: str) -> List[Dict[str, Any]]:
        """Parse plain text or markdown using AI."""
        
        system_prompt = """You are a task extraction expert. Extract development tasks from the given text.
For each task, identify:
- title: Short task name
- description: Detailed description
- priority: high, medium, or low (infer from context)
- estimated_effort: Time estimate if mentioned
- labels: Relevant tags (e.g., frontend, backend, database)
- dependencies: Other tasks this depends on (by title)
- notes: Any additional context

Return ONLY a valid JSON array of tasks. No markdown, no explanations, just the JSON array."""

        user_prompt = f"""Extract all development tasks from this text:

{text}

Return a JSON array of tasks with this structure:
[
  {{
    "title": "Task title",
    "description": "Task description",
    "priority": "high|medium|low",
    "estimated_effort": "time estimate",
    "labels": ["tag1", "tag2"],
    "dependencies": ["other task title"],
    "notes": "additional context"
  }}
]

JSON array:"""

        try:
            response = self.ollama.generate(user_prompt, system=system_prompt)
            
            # Extract JSON from response
            json_str = self._extract_json(response)
            tasks = json.loads(json_str)
            
            # Validate and clean tasks
            return self._validate_tasks(tasks)
        
        except Exception as e:
            raise Exception(f"Error parsing text with AI: {str(e)}")
    
    def parse_json(self, file_content: bytes) -> List[Dict[str, Any]]:
        """Parse JSON file."""
        try:
            data = json.loads(file_content.decode('utf-8'))
            
            # Handle different JSON structures
            if isinstance(data, list):
                tasks = data
            elif isinstance(data, dict) and 'tasks' in data:
                tasks = data['tasks']
            else:
                raise ValueError("JSON must be an array or have a 'tasks' key")
            
            return self._validate_tasks(tasks)
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")
    
    def parse_csv(self, file_content: bytes) -> List[Dict[str, Any]]:
        """Parse CSV file."""
        try:
            text = file_content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(text))
            tasks = []
            
            for row in reader:
                task = {
                    'title': row.get('title', row.get('Title', '')),
                    'description': row.get('description', row.get('Description', '')),
                    'priority': row.get('priority', row.get('Priority', 'medium')).lower(),
                    'estimated_effort': row.get('estimated_effort', row.get('Effort', '')),
                    'labels': self._parse_list_field(row.get('labels', row.get('Labels', ''))),
                    'dependencies': self._parse_list_field(row.get('dependencies', row.get('Dependencies', ''))),
                    'notes': row.get('notes', row.get('Notes', ''))
                }
                tasks.append(task)
            
            return self._validate_tasks(tasks)
        
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")
    
    def parse_excel(self, file_content: bytes) -> List[Dict[str, Any]]:
        """Parse Excel file."""
        try:
            df = pd.read_excel(io.BytesIO(file_content))
            tasks = []
            
            for _, row in df.iterrows():
                task = {
                    'title': str(row.get('title', row.get('Title', ''))),
                    'description': str(row.get('description', row.get('Description', ''))),
                    'priority': str(row.get('priority', row.get('Priority', 'medium'))).lower(),
                    'estimated_effort': str(row.get('estimated_effort', row.get('Effort', ''))),
                    'labels': self._parse_list_field(str(row.get('labels', row.get('Labels', '')))),
                    'dependencies': self._parse_list_field(str(row.get('dependencies', row.get('Dependencies', '')))),
                    'notes': str(row.get('notes', row.get('Notes', '')))
                }
                tasks.append(task)
            
            return self._validate_tasks(tasks)
        
        except Exception as e:
            raise ValueError(f"Error parsing Excel: {str(e)}")
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON array from text that might contain markdown or other content."""
        # Try to find JSON array
        start = text.find('[')
        end = text.rfind(']') + 1
        
        if start != -1 and end > start:
            return text[start:end]
        
        # If no array found, try to find JSON object
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start != -1 and end > start:
            return text[start:end]
        
        return text
    
    def _parse_list_field(self, value: str) -> List[str]:
        """Parse comma-separated string into list."""
        if not value or value == 'nan':
            return []
        return [item.strip() for item in str(value).split(',') if item.strip()]
    
    def _validate_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and clean task data."""
        validated = []
        
        for task in tasks:
            if not isinstance(task, dict):
                continue
            
            # Ensure required fields
            if not task.get('title'):
                continue
            
            validated_task = {
                'title': str(task.get('title', '')).strip(),
                'description': str(task.get('description', '')).strip(),
                'priority': str(task.get('priority', 'medium')).lower(),
                'estimated_effort': str(task.get('estimated_effort', '')).strip(),
                'labels': task.get('labels', []) if isinstance(task.get('labels'), list) else [],
                'dependencies': task.get('dependencies', []) if isinstance(task.get('dependencies'), list) else [],
                'notes': str(task.get('notes', '')).strip(),
                'status': 'pending'
            }
            
            # Validate priority
            if validated_task['priority'] not in ['high', 'medium', 'low']:
                validated_task['priority'] = 'medium'
            
            validated.append(validated_task)
        
        return validated


def test_parser():
    """Test the parser with sample data."""
    parser = TaskParser()
    
    # Test text parsing
    sample_text = """
    Task 1: Setup Database
    Description: Create PostgreSQL schema for the application
    Priority: High
    Effort: 3 days
    
    Task 2: Build API
    Description: Create REST API endpoints
    Priority: High
    Depends on: Setup Database
    Effort: 5 days
    """
    
    try:
        tasks = parser.parse_text(sample_text)
        print(f"Parsed {len(tasks)} tasks:")
        for task in tasks:
            print(f"  - {task['title']}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_parser()

# Made with Bob
