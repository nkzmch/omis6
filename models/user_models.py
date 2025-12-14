from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4
from .enums import UserRole

@dataclass
class User:
    """Пользователь системы"""
    id: str = field(default_factory=lambda: str(uuid4()))
    username: str = ""
    role: UserRole = UserRole.USER
    preferences: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class UserQuery:
    """Запрос пользователя"""
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    text: str = ""
    query_type: str = "SEARCH"
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SearchResult:
    """Результат поиска"""
    id: str = field(default_factory=lambda: str(uuid4()))
    query_id: str = ""
    title: str = ""
    snippet: str = ""
    relevance: float = 0.0
    data_type: str = "DOCUMENT"
    source: str = ""

@dataclass
class Report:
    """Аналитический отчет"""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    content: Any = None
    format: str = "PDF"
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)
