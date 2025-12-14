from enum import Enum

class DataSourceType(Enum):
    SQL = "SQL"
    NOSQL = "NOSQL"
    FILE = "FILE"
    API = "API"
    STREAM = "STREAM"

class StorageType(Enum):
    RELATIONAL = "RELATIONAL"
    DOCUMENT = "DOCUMENT"
    GRAPH = "GRAPH"

class UserRole(Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    USER = "USER"
    DEVELOPER = "DEVELOPER"

class EntityType(Enum):
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    DATE = "DATE"
    CONCEPT = "CONCEPT"

class RelationType(Enum):
    IS_A = "IS_A"
    PART_OF = "PART_OF"
    RELATED_TO = "RELATED_TO"
    LOCATED_IN = "LOCATED_IN"
