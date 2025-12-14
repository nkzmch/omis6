"""
Веб-интерфейс системы управления знаниями - УПРОЩЕННАЯ РАБОЧАЯ ВЕРСИЯ
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sys
import os
from datetime import datetime

# Добавляем путь к модулям системы
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    # Импортируем минимальный набор
    from models.enums import UserRole
    from models.user_models import User
    from models.data_models import KnowledgeGraph, Entity
    from models.enums import EntityType
    
    from services.data_service import StorageService
    from services.analysis_service import NLPService
    from services.ui_service import SearchService, ChatbotService, ReportService
    
    print("✅ Все модули системы загружены")
except ImportError as e:
    print(f"⚠️  Предупреждение: {e}")
    print("Работаем в демо-режиме")

app = Flask(__name__)
app.secret_key = 'knowledge_management_secret_key_123'
app.config['SESSION_TYPE'] = 'filesystem'

# Инициализация сервисов
try:
    storage_service = StorageService()
    nlp_service = NLPService()
    search_service = SearchService(storage_service, nlp_service)
    chatbot_service = ChatbotService(search_service)
    report_service = ReportService()
    services_loaded = True
except:
    services_loaded = False
    print("⚠️  Сервисы инициализированы в демо-режиме")

# Демо-данные
def init_demo_data():
    """Инициализация демонстрационных данных"""
    if not services_loaded:
        return
    
    # Создаем демонстрационный граф знаний
    demo_graph = KnowledgeGraph(
        name="Технологические компании",
        entities=[
            Entity(name="Microsoft", entity_type=EntityType.ORGANIZATION),
            Entity(name="Windows 11", entity_type=EntityType.CONCEPT),
            Entity(name="Искусственный интеллект", entity_type=EntityType.CONCEPT),
            Entity(name="Сиэтл", entity_type=EntityType.LOCATION),
            Entity(name="Сатья Наделла", entity_type=EntityType.PERSON),
        ]
    )
    
    # Дополнительные графы
    project_graph = KnowledgeGraph(
        name="Проект СистемаХ",
        entities=[
            Entity(name="Иван Петров", entity_type=EntityType.PERSON),
            Entity(name="ТехноИнновации", entity_type=EntityType.ORGANIZATION),
            Entity(name="Анализ рисков", entity_type=EntityType.CONCEPT),
            Entity(name="Отчет Q4 2024", entity_type=EntityType.CONCEPT),
        ]
    )
    
    storage_service.save_graph(demo_graph)
    storage_service.save_graph(project_graph)
    print(f"✅ Демо-данные загружены: {len(storage_service.graphs)} графов")

# Инициализируем данные
init_demo_data()

# ========== МАРШРУТЫ ==========

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            user = User(username=username, role=UserRole.USER)
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role.value
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Панель управления"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Статистика системы
    stats = {
        'graphs_count': len(storage_service.graphs) if services_loaded else 2,
        'total_entities': sum(len(g.entities) for g in storage_service.graphs.values()) if services_loaded else 9,
        'documents_count': len(storage_service.documents) if services_loaded else 5,
        'username': session.get('username', 'Гость')
    }
    
    return render_template('dashboard.html', 
                         stats=stats,
                         username=session.get('username'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Страница поиска"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    results = []
    query = ""
    
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query and services_loaded:
            from models.user_models import UserQuery as UQ
            user_query = UQ(
                user_id=session['user_id'],
                text=query,
                query_type="SEARCH"
            )
            results = search_service.semantic_search(user_query)
    
    return render_template('search.html', 
                         query=query, 
                         results=results,
                         username=session.get('username'))

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    """Интерфейс чат-бота"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    message_history = []
    
    if services_loaded:
        message_history = chatbot_service.get_conversation_history(user_id)
    
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        if message and services_loaded:
            response = chatbot_service.process_message(user_id, message)
            message_history = chatbot_service.get_conversation_history(user_id)
    
    return render_template('chatbot.html', 
                         history=message_history or [],
                         username=session.get('username'))

@app.route('/nlp-analysis', methods=['GET', 'POST'])
def nlp_analysis():
    """Страница NLP-анализа"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    entities = []
    sentiment = 0.5
    analyzed_text = ""
    
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        analyzed_text = text
        
        if text and services_loaded:
            entities = nlp_service.extract_entities(text)
            sentiment = nlp_service.analyze_sentiment(text)
    
    return render_template('nlp_analysis.html',
                         text=analyzed_text,
                         entities=entities,
                         sentiment=sentiment,
                         username=session.get('username'))

@app.route('/knowledge-graphs')
def knowledge_graphs():
    """Просмотр графов знаний"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    graphs = []
    if services_loaded:
        graphs = list(storage_service.graphs.values())
    
    return render_template('knowledge_graphs.html', 
                         graphs=graphs,
                         username=session.get('username'))

@app.route('/reports')
def reports():
    """Генерация отчетов"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('reports.html',
                         username=session.get('username'))

@app.route('/system-info')
def system_info():
    """Информация о системе"""
    return render_template('system_info.html',
                         username=session.get('username'))

@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Выход</title></head>
    <body style="text-align: center; padding: 50px;">
        <h1>Вы вышли из системы</h1>
        <p><a href="/">Вернуться на главную</a></p>
    </body>
    </html>
    '''

# ========== API ЭНДПОИНТЫ ==========

@app.route('/api/status')
def api_status():
    """API: статус системы"""
    return jsonify({
        'status': 'active',
        'version': '1.0',
        'services_loaded': services_loaded,
        'user': session.get('username'),
        'graphs_count': len(storage_service.graphs) if services_loaded else 0,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API для чат-бота"""
    if not services_loaded:
        return jsonify({
            'success': False,
            'response': 'Сервисы не загружены'
        })
    
    data = request.json
    message = data.get('message', '')
    user_id = session.get('user_id', 'anonymous')
    
    response = chatbot_service.process_message(user_id, message)
    history = chatbot_service.get_conversation_history(user_id)
    
    return jsonify({
        'success': True,
        'response': response,
        'history': history[-5:] if history else []
    })

# ========== ЗАПУСК СЕРВЕРА ==========

if __name__ == '__main__':
    print("="*60)
    print("🌐 ВЕБ-ИНТЕРФЕЙС СИСТЕМЫ УПРАВЛЕНИЯ ЗНАНИЯМИ")
    print("="*60)
    print("Сервер запускается на http://localhost:5000")
    print("Доступные страницы:")
    print("• / - Главная страница (вход)")
    print("• /dashboard - Панель управления")
    print("• /search - Поиск знаний (попробуйте 'Microsoft' или 'проект')")
    print("• /knowledge-graphs - Графы знаний")
    print("• /chatbot - Интеллектуальный чат-бот")
    print("• /nlp-analysis - NLP анализ текста")
    print("• /api/status - API статуса системы")
    print("="*60)
    
    app.run(debug=True, port=5000)