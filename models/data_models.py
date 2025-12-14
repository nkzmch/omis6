from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4
from .enums import DataSourceType, StorageType, EntityType, RelationType

@dataclass
class RawData:
    """Сырые данные"""
    id: str = field(default_factory=lambda: str(uuid4()))
    source_type: DataSourceType = DataSourceType.FILE
    content: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class TransformedData:
    """Трансформированные данные"""
    id: str = field(default_factory=lambda: str(uuid4()))
    source_id: Optional[str] = None
    content: Any = None
    format: str = "JSON"
    storage_type: StorageType = StorageType.DOCUMENT
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Entity:
    """Семантическая сущность"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    entity_type: EntityType = EntityType.CONCEPT
    confidence: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Relation:
    """Отношение между сущностями"""
    id: str = field(default_factory=lambda: str(uuid4()))
    source_entity_id: str = ""
    target_entity_id: str = ""
    relation_type: RelationType = RelationType.RELATED_TO
    strength: float = 1.0

@dataclass
class KnowledgeGraph:
    """Граф знаний"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    entities: List[Entity] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Connection:
    """Подключение к источнику"""
    id: str = field(default_factory=lambda: str(uuid4()))
    source_type: DataSourceType = DataSourceType.SQL
    connection_string: str = ""
    is_active: bool = False
    last_used: datetime = field(default_factory=datetime.now)
