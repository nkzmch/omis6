"""
Главный файл системы управления знаниями
Версия без __init__.py файлов
"""
import sys
import os

print("="*60)
print("🚀 СИСТЕМА УПРАВЛЕНИЯ ЗНАНИЯМИ")
print("="*60)

# Добавляем текущую папку в путь Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Импортируем напрямую без __init__.py
    import models.enums as enums
    import models.data_models as data_models
    import models.user_models as user_models
    import services.data_service as data_service
    import services.analysis_service as analysis_service
    import services.ui_service as ui_service
    
    print("✅ Все модули успешно импортированы")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    sys.exit(1)

def main():
    """Основная демонстрация"""
    print("\n📊 ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ")
    print("-" * 40)
    
    # Используем классы через модули
    DataSourceType = enums.DataSourceType
    StorageType = enums.StorageType
    UserRole = enums.UserRole
    EntityType = enums.EntityType
    
    # 1. Создаем пользователя
    user = user_models.User(
        username="analyst_1",
        role=UserRole.ANALYST
    )
    print(f"1. Создан пользователь: {user.username}")
    
    # 2. Создаем подключение
    conn = data_models.Connection(
        source_type=DataSourceType.SQL,
        connection_string="localhost/db"
    )
    print(f"2. Создано подключение: {conn.connection_string}")
    
    # 3. Создаем ETL сервис
    etl = data_service.ETLService()
    etl.add_source(conn)
    etl.add_loader(StorageType.DOCUMENT)
    print("3. Настроен ETL сервис")
    
    # 4. Запускаем ETL
    result = etl.run_etl()
    print(f"4. ETL выполнен: {result['loaded']} данных загружено")
    
    # 5. Анализ текста
    nlp = analysis_service.NLPService()
    text = "Компания Microsoft в Сиэтле представила Windows 11 15.12.2024"
    entities = nlp.extract_entities(text)
    print(f"5. NLP анализ: найдено {len(entities)} сущностей")
    
    # 6. Строим граф знаний
    builder = analysis_service.KnowledgeBuilder()
    relations = builder.build_relations(entities, text)
    graph = builder.create_knowledge_graph(
        name="Технологический граф",
        entities=entities,
        relations=relations
    )
    print(f"6. Построен граф знаний: {graph.name}")
    
    # 7. Сохраняем граф
    storage = data_service.StorageService()
    storage.save_graph(graph)
    print("7. Граф сохранен в хранилище")
    
    # 8. Поиск
    search = ui_service.SearchService(storage, nlp)
    query = user_models.UserQuery(
        user_id=user.id,
        text="Microsoft Windows"
    )
    results = search.semantic_search(query)
    print(f"8. Поиск выполнен: {len(results)} результатов")
    
    # 9. Чат-бот
    chatbot = ui_service.ChatbotService(search)
    response = chatbot.process_message(user.id, "Привет, найди информацию о Microsoft")
    print(f"9. Чат-бот: {response}")
    
    # 10. Генерация гипотез
    hypothesis = analysis_service.HypothesisGenerator()
    hypotheses = hypothesis.generate_hypotheses(graph)
    print(f"10. Сгенерировано гипотез: {len(hypotheses)}")
    
    print("\n" + "="*60)
    print("📈 ИТОГОВАЯ СТАТИСТИКА")
    print("="*60)
    print(f"• Пользователей: 1")
    print(f"• Графов знаний: 1")
    print(f"• Сущностей: {len(entities)}")
    print(f"• Отношений: {len(relations)}")
    print(f"• Результатов поиска: {len(results)}")
    print(f"• Гипотез: {len(hypotheses)}")
    
    print("\n" + "="*60)
    print("✅ СИСТЕМА УСПЕШНО РАБОТАЕТ!")
    print("="*60)

if __name__ == "__main__":
    main()