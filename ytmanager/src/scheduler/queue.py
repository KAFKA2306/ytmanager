from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionQueue:
    def __init__(self, queue_file: str = "data/execution_queue.json"):
        self.queue_file = Path(queue_file)
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        self.queue = self._load()

    def _load(self) -> List[Dict]:
        if self.queue_file.exists():
            with open(self.queue_file) as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.queue_file, "w") as f:
            json.dump(self.queue, f, indent=2, ensure_ascii=False)

    def add(self, channel: str, command: str, priority: int = 0, metadata: Optional[Dict] = None) -> str:
        task_id = f"{channel}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        task = {
            "task_id": task_id,
            "channel": channel,
            "command": command,
            "priority": priority,
            "status": TaskStatus.PENDING,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "error": None
        }
        self.queue.append(task)
        self._sort()
        self._save()
        return task_id

    def _sort(self):
        self.queue.sort(key=lambda t: (t["priority"], t["created_at"]), reverse=True)

    def get_next(self) -> Optional[Dict]:
        for task in self.queue:
            if task["status"] == TaskStatus.PENDING:
                return task
        return None

    def start(self, task_id: str):
        task = self._find(task_id)
        if task:
            task["status"] = TaskStatus.RUNNING
            task["started_at"] = datetime.now().isoformat()
            self._save()

    def complete(self, task_id: str):
        task = self._find(task_id)
        if task:
            task["status"] = TaskStatus.COMPLETED
            task["completed_at"] = datetime.now().isoformat()
            self._save()

    def fail(self, task_id: str, error: str):
        task = self._find(task_id)
        if task:
            task["status"] = TaskStatus.FAILED
            task["completed_at"] = datetime.now().isoformat()
            task["error"] = error
            self._save()

    def _find(self, task_id: str) -> Optional[Dict]:
        for task in self.queue:
            if task["task_id"] == task_id:
                return task
        return None

    def is_running(self, channel: str) -> bool:
        for task in self.queue:
            if task["channel"] == channel and task["status"] == TaskStatus.RUNNING:
                return True
        return False

    def list(self, status: Optional[TaskStatus] = None) -> List[Dict]:
        if status:
            return [t for t in self.queue if t["status"] == status]
        return self.queue

    def cleanup(self, keep_recent: int = 100):
        completed = [t for t in self.queue if t["status"] in [TaskStatus.COMPLETED, TaskStatus.FAILED]]
        completed.sort(key=lambda t: t["completed_at"] or "", reverse=True)

        to_keep = set(t["task_id"] for t in completed[:keep_recent])
        self.queue = [t for t in self.queue if t["status"] in [TaskStatus.PENDING, TaskStatus.RUNNING] or t["task_id"] in to_keep]
        self._save()
