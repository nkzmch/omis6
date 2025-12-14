import re
from typing import List, Dict, Any, Tuple
from models.data_models import Entity, Relation, KnowledgeGraph
from models.enums import EntityType, RelationType

class NLPService:
    """Обработка естественного языка"""
    
    def __init__(self):
        self.entity_patterns = {
            EntityType.PERSON: r'\b([А-Я][а-я]+ [А-Я][а-я]+)\b',
            EntityType.ORGANIZATION: r'\b(ООО|АО|ЗАО|ИП)\s+[«"][^«"]+[»"]',
            EntityType.LOCATION: r'\b(г\.|гор\.|город)\s+[А-Я][а-я]+\b',
            EntityType.DATE: r'\b(\d{1,2}\.\d{1,2}\.\d{4}|\d{4}\s+год)\b'
        }
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Извлечь сущности из текста"""
        entities = []
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity = Entity(
                    name=match.group(),
                    entity_type=entity_type,
                    confidence=0.9
                )
                entities.append(entity)
        
        # Извлечение концептов по ключевым словам
        concept_keywords = ['проект', 'риск', 'отчет', 'анализ', 'данные']
        for keyword in concept_keywords:
            if keyword.lower() in text.lower():
                entity = Entity(
                    name=keyword.capitalize(),
                    entity_type=EntityType.CONCEPT,
                    confidence=0.7
                )
                entities.append(entity)
        
        print(f"Извлечено {len(entities)} сущностей")
        return entities
    
    def analyze_sentiment(self, text: str) -> float:
        """Проанализировать тональность текста"""
        positive_words = ['успех', 'хорошо', 'отлично', 'рекомендую', 'эффективный']
        negative_words = ['проблема', 'риск', 'плохо', 'ошибка', 'негативный']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.5  # Нейтральная
        
        return positive_count / total

class KnowledgeBuilder:
    """Построитель знаний"""
    
    def __init__(self):
        self.relations: List[Relation] = []
    
    def build_relations(self, entities: List[Entity], text: str) -> List[Relation]:
        """Построить отношения между сущностями"""
        relations = []
        
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities):
                if i != j:
                    # Простая эвристика: сущности в одном предложении связаны
                    if entity1.name in text and entity2.name in text:
                        relation = Relation(
                            source_entity_id=entity1.id,
                            target_entity_id=entity2.id,
                            relation_type=RelationType.RELATED_TO,
                            strength=0.8
                        )
                        relations.append(relation)
        
        print(f"Построено {len(relations)} отношений")
        return relations
    
    def create_knowledge_graph(self, name: str, 
                              entities: List[Entity], 
                              relations: List[Relation]) -> KnowledgeGraph:
        """Создать граф знаний"""
        graph = KnowledgeGraph(
            name=name,
            entities=entities,
            relations=relations
        )
        
        print(f"Создан граф знаний: {name}")
        return graph

class HypothesisGenerator:
    """Генератор гипотез"""
    
    def generate_hypotheses(self, graph: KnowledgeGraph) -> List[str]:
        """Сгенерировать гипотезы на основе графа знаний"""
        hypotheses = []
        
        # Анализ связей
        entity_count = len(graph.entities)
        relation_count = len(graph.relations)
        
        if relation_count > entity_count * 2:
            hypotheses.append("Высокая связность данных может указывать на системные зависимости")
        
        # Поиск центральных сущностей
        relation_counts = {}
        for relation in graph.relations:
            relation_counts[relation.source_entity_id] = \
                relation_counts.get(relation.source_entity_id, 0) + 1
        
        if relation_counts:
            max_entity_id = max(relation_counts, key=relation_counts.get)
            max_entity = next(e for e in graph.entities if e.id == max_entity_id)
            hypotheses.append(f"Сущность '{max_entity.name}' является центральной в системе")
        
        # Поиск паттернов
        person_entities = [e for e in graph.entities if e.entity_type == EntityType.PERSON]
        org_entities = [e for e in graph.entities if e.entity_type == EntityType.ORGANIZATION]
        
        if person_entities and org_entities:
            hypotheses.append(f"Обнаружены связи между {len(person_entities)} людьми и {len(org_entities)} организациями")
        
        return hypotheses
