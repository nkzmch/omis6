from datetime import datetime
from typing import List, Dict, Any, Optional
from models.data_models import RawData, TransformedData, Entity, Relation, KnowledgeGraph, Connection
from models.enums import DataSourceType, StorageType, EntityType, RelationType
class DataExtractor:
    """Извлекает данные из источников"""
    
    def __init__(self, connection: Connection):
        self.connection = connection
    
    def extract(self) -> List[RawData]:
        """Извлечь данные из источника"""
        print(f"Извлечение данных из {self.connection.source_type.value}")
        
        # Имитация извлечения данных
        data = RawData(
            source_type=self.connection.source_type,
            content={"sample": "data", "value": 42},
            metadata={"source": self.connection.connection_string}
        )
        
        return [data]
    
    def test_connection(self) -> bool:
        """Проверить подключение"""
        try:
            self.connection.is_active = True
            self.connection.last_used = datetime.now()
            return True
        except:
            self.connection.is_active = False
            return False

class DataTransformer:
    """Трансформирует данные"""
    
    def __init__(self):
        self.rules: List[str] = []
    
    def transform(self, raw_data: RawData) -> TransformedData:
        """Трансформировать сырые данные"""
        print(f"Трансформация данных {raw_data.id}")
        
        # Простая трансформация
        transformed = TransformedData(
            source_id=raw_data.id,
            content=raw_data.content,
            format="JSON",
            storage_type=StorageType.DOCUMENT,
            metadata={
                **raw_data.metadata,
                "transformed_at": datetime.now().isoformat()
            }
        )
        
        return transformed
    
    def add_rule(self, rule: str):
        """Добавить правило трансформации"""
        self.rules.append(rule)

class DataLoader:
    """Загружает данные в хранилища"""
    
    def __init__(self, storage_type: StorageType):
        self.storage_type = storage_type
        self.data_store: Dict[str, Any] = {}
    
    def load(self, data: TransformedData) -> bool:
        """Загрузить данные"""
        print(f"Загрузка данных {data.id} в {self.storage_type.value}")
        
        # Имитация загрузки
        self.data_store[data.id] = data
        return True
    
    def retrieve(self, data_id: str) -> Optional[TransformedData]:
        """Получить данные по ID"""
        return self.data_store.get(data_id)

class ETLService:
    """Оркестратор ETL-процессов"""
    
    def __init__(self):
        self.extractors: List[DataExtractor] = []
        self.transformer = DataTransformer()
        self.loaders: Dict[StorageType, DataLoader] = {}
    
    def add_source(self, connection: Connection):
        """Добавить источник данных"""
        extractor = DataExtractor(connection)
        self.extractors.append(extractor)
        print(f"Добавлен источник: {connection.connection_string}")
    
    def add_loader(self, storage_type: StorageType):
        """Добавить загрузчик"""
        loader = DataLoader(storage_type)
        self.loaders[storage_type] = loader
    
    def run_etl(self) -> Dict[str, Any]:
        """Запустить ETL-процесс"""
        results = {
            "extracted": 0,
            "transformed": 0,
            "loaded": 0,
            "errors": []
        }
        
        try:
            # Извлечение
            all_raw_data = []
            for extractor in self.extractors:
                if extractor.test_connection():
                    data = extractor.extract()
                    all_raw_data.extend(data)
                    results["extracted"] += len(data)
            
            # Трансформация
            transformed_data = []
            for raw_data in all_raw_data:
                transformed = self.transformer.transform(raw_data)
                transformed_data.append(transformed)
                results["transformed"] += 1
            
            # Загрузка
            for data in transformed_data:
                storage_type = data.storage_type
                if storage_type in self.loaders:
                    success = self.loaders[storage_type].load(data)
                    if success:
                        results["loaded"] += 1
            
            print(f"ETL завершен: {results}")
            return results
            
        except Exception as e:
            results["errors"].append(str(e))
            print(f"Ошибка ETL: {e}")
            return results

class StorageService:
    """Управление хранилищами данных"""
    
    def __init__(self):
        self.graphs: Dict[str, KnowledgeGraph] = {}
        self.documents: Dict[str, TransformedData] = {}
    
    def save_graph(self, graph: KnowledgeGraph) -> str:
        """Сохранить граф знаний"""
        self.graphs[graph.id] = graph
        print(f"Граф сохранен: {graph.name}")
        return graph.id
    
    def get_graph(self, graph_id: str) -> Optional[KnowledgeGraph]:
        """Получить граф по ID"""
        return self.graphs.get(graph_id)
    
    def find_entities(self, entity_type: Optional[EntityType] = None) -> List[Entity]:
        """Найти сущности по типу"""
        entities = []
        for graph in self.graphs.values():
            for entity in graph.entities:
                if entity_type is None or entity.entity_type == entity_type:
                    entities.append(entity)
        return entities
    
    def save_document(self, data: TransformedData) -> str:
        """Сохранить документ"""
        self.documents[data.id] = data
        return data.id
