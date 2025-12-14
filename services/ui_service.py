from typing import List, Dict, Any, Optional
from datetime import datetime
from models.user_models import User, UserQuery, SearchResult, Report
from models.data_models import KnowledgeGraph
from models.enums import EntityType
class SearchService:
    """Сервис поиска"""
    
    def __init__(self, storage_service, analysis_service):
        self.storage_service = storage_service
        self.analysis_service = analysis_service
    
    def semantic_search(self, query: UserQuery) -> List[SearchResult]:
        """Семантический поиск"""
        print(f"Семантический поиск: {query.text}")
        
        results = []
        
        # Поиск в графах знаний
        for graph_id, graph in self.storage_service.graphs.items():
            relevance = self._calculate_relevance(graph, query.text)
            if relevance > 0:
                result = SearchResult(
                    query_id=query.id,
                    title=graph.name,
                    snippet=f"Граф знаний с {len(graph.entities)} сущностями",
                    relevance=relevance,
                    data_type="GRAPH",
                    source="knowledge_base"
                )
                results.append(result)
        
        # Поиск в документах
        for doc_id, doc in self.storage_service.documents.items():
            if query.text.lower() in str(doc.content).lower():
                result = SearchResult(
                    query_id=query.id,
                    title=f"Документ {doc.id[:8]}",
                    snippet=str(doc.content)[:100] + "...",
                    relevance=0.7,
                    data_type="DOCUMENT",
                    source="document_store"
                )
                results.append(result)
        
        # Сортировка по релевантности
        results.sort(key=lambda x: x.relevance, reverse=True)
        
        return results[:10]  # Возвращаем топ-10 результатов
    
    def _calculate_relevance(self, graph: KnowledgeGraph, query: str) -> float:
        """Рассчитать релевантность графа запросу"""
        relevance = 0.0
        
        # Проверка названия
        if query.lower() in graph.name.lower():
            relevance += 0.5
        
        # Проверка сущностей
        for entity in graph.entities:
            if query.lower() in entity.name.lower():
                relevance += 0.3
                break
        
        # Проверка типа сущностей
        query_lower = query.lower()
        if any(word in query_lower for word in ['человек', 'персона', 'сотрудник']):
            if any(e.entity_type == EntityType.PERSON for e in graph.entities):
                relevance += 0.2
        
        if any(word in query_lower for word in ['компания', 'организация', 'фирма']):
            if any(e.entity_type == EntityType.ORGANIZATION for e in graph.entities):
                relevance += 0.2
        
        return min(relevance, 1.0)  # Ограничиваем максимум 1.0
    
    def suggest_queries(self, partial_query: str) -> List[str]:
        """Предложить варианты запросов"""
        suggestions = [
            "Найди отчеты по проекту",
            "Показать связи между организациями",
            "Анализ рисков",
            "Статистика за последний год",
            "Граф знаний по теме"
        ]
        
        # Фильтруем по частичному запросу
        filtered = [s for s in suggestions if partial_query.lower() in s.lower()]
        
        # Добавляем общие предложения
        if len(filtered) < 3:
            filtered.extend(suggestions[:3-len(filtered)])
        
        return filtered

class ReportService:
    """Сервис генерации отчетов"""
    
    def generate_report(self, title: str, content: Any, 
                       user_id: str, format: str = "TEXT") -> Report:
        """Сгенерировать отчет"""
        report = Report(
            title=title,
            content=content,
            format=format,
            created_by=user_id
        )
        
        print(f"Сгенерирован отчет: {title}")
        return report
    
    def export_report(self, report: Report, export_format: str) -> Dict[str, Any]:
        """Экспортировать отчет в другой формат"""
        return {
            "report_id": report.id,
            "title": report.title,
            "format": export_format,
            "content": f"Экспортированный отчет: {report.title}",
            "exported_at": datetime.now().isoformat()
        }

class ChatbotService:
    """Чат-бот для интерфейса"""
    
    def __init__(self, search_service):
        self.search_service = search_service
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def process_message(self, user_id: str, message: str) -> str:
        """Обработать сообщение пользователя"""
        # Сохраняем историю
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "role": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Простая логика ответов
        if "привет" in message.lower():
            response = "Привет! Я могу помочь вам найти информацию в системе знаний."
        elif "найди" in message.lower() or "поиск" in message.lower():
            query = UserQuery(
                user_id=user_id,
                text=message,
                query_type="SEARCH"
            )
            results = self.search_service.semantic_search(query)
            response = f"Найдено {len(results)} результатов по вашему запросу."
        elif "отчет" in message.lower():
            response = "Я могу помочь сгенерировать отчет. Укажите параметры отчета."
        elif "помощь" in message.lower():
            response = "Доступные команды: поиск, отчет, анализ, граф знаний"
        else:
            response = "Я понял ваш запрос. Уточните, пожалуйста, что именно вас интересует?"
        
        # Сохраняем ответ
        self.conversation_history[user_id].append({
            "role": "assistant",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Получить историю разговора"""
        return self.conversation_history.get(user_id, [])
