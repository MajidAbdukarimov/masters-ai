import logging
import os
import sys
from datetime import datetime

# Настройка логгера с элегантным форматированием
def setup_logging(log_file="app.log", log_level=logging.INFO):
    """
    Настраивает систему логирования с элегантным форматированием
    
    :param log_file: Имя файла для записи логов
    :param log_level: Уровень логирования
    """
    # Создаем форматтер для консоли и файла
    console_format = "%(asctime)s | %(levelname)-8s | %(message)s"
    file_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Настройка корневого логгера
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Удаляем существующие обработчики, если они есть
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Создаем обработчик для вывода в файл
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(file_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Не удалось настроить файловый логгер: {e}")
    
    # Создаем обработчик для вывода в консоль с цветами
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(console_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Логируем начало сессии
    logging.info("Logging system initialized with elegant formatting")
    
    return logger

# Глобальный логгер
logger = setup_logging()

# Функции для разных уровней логирования
def log_info(info_message):
    """
    Логирование информационного сообщения
    
    :param info_message: Текст сообщения
    """
    logger.info(f"[INFO] {info_message}")

def log_warning(warning_message):
    """
    Логирование предупреждения
    
    :param warning_message: Текст предупреждения
    """
    logger.warning(f"[WARNING] {warning_message}")

def log_error(error_message, exc_info=None):
    """
    Логирование ошибки
    
    :param error_message: Текст ошибки
    :param exc_info: Информация об исключении (если есть)
    """
    if exc_info:
        logger.error(f"[ERROR] {error_message}", exc_info=exc_info)
    else:
        logger.error(f"[ERROR] {error_message}")

def log_debug(debug_message):
    """
    Логирование отладочного сообщения
    
    :param debug_message: Текст отладочного сообщения
    """
    logger.debug(f"[DEBUG] {debug_message}")

def log_critical(critical_message):
    """
    Логирование критической ошибки
    
    :param critical_message: Текст критической ошибки
    """
    logger.critical(f"[CRITICAL] {critical_message}")

def log_event(event_type, event_message):
    """
    Логирование событий приложения
    
    :param event_type: Тип события
    :param event_message: Сообщение о событии
    """
    logger.info(f"[EVENT] {event_type}: {event_message}")

def log_query(query_text, user_id=None):
    """
    Логирование запроса пользователя
    
    :param query_text: Текст запроса
    :param user_id: ID пользователя (если доступен)
    """
    user_info = f"User {user_id}" if user_id else "Anonymous user"
    logger.info(f"[QUERY] {user_info} - '{query_text}'")

def log_response(response_text, response_time=None):
    """
    Логирование ответа системы
    
    :param response_text: Текст ответа
    :param response_time: Время ответа в мс (если доступно)
    """
    time_info = f" (took {response_time}ms)" if response_time else ""
    # Усекаем ответ, если он слишком длинный
    if len(response_text) > 100:
        response_text = response_text[:100] + "..."
    logger.info(f"[RESPONSE]{time_info} '{response_text}'")

def log_db_query(query, params=None):
    """
    Логирование запроса к базе данных
    
    :param query: SQL запрос
    :param params: Параметры запроса (если есть)
    """
    # Усекаем запрос, если он слишком длинный
    if len(query) > 200:
        query = query[:200] + "..."
    
    if params:
        logger.debug(f"[DB] Executing query: {query} with params: {params}")
    else:
        logger.debug(f"[DB] Executing query: {query}")

def log_db_result(result, query_time=None):
    """
    Логирование результата запроса к БД
    
    :param result: Результат запроса
    :param query_time: Время выполнения запроса в мс (если доступно)
    """
    time_info = f" (took {query_time}ms)" if query_time else ""
    
    # Определяем тип результата и форматируем информацию соответственно
    if isinstance(result, int):
        logger.debug(f"[DB]{time_info} Affected rows: {result}")
    elif hasattr(result, '__len__'):
        logger.debug(f"[DB]{time_info} Returned {len(result)} rows")
    else:
        logger.debug(f"[DB]{time_info} Query executed")

def log_api_request(endpoint, method="GET", params=None):
    """
    Логирование запроса к API
    
    :param endpoint: Конечная точка API
    :param method: HTTP метод
    :param params: Параметры запроса (если есть)
    """
    if params:
        logger.info(f"[API] {method} request to {endpoint} with params: {params}")
    else:
        logger.info(f"[API] {method} request to {endpoint}")

def log_api_response(response, request_time=None, status_code=None):
    """
    Логирование ответа от API
    
    :param response: Ответ от API
    :param request_time: Время запроса в мс (если доступно)
    :param status_code: HTTP статус код (если доступен)
    """
    time_info = f" (took {request_time}ms)" if request_time else ""
    status_info = f" [Status: {status_code}]" if status_code else ""
    
    # Усекаем ответ, если он слишком длинный
    if isinstance(response, str) and len(response) > 100:
        response = response[:100] + "..."
    
    logger.info(f"[API]{status_info}{time_info} Response received")

def log_user_action(user_id, action, details=None):
    """
    Логирование действий пользователя
    
    :param user_id: ID пользователя
    :param action: Выполненное действие
    :param details: Детали действия (если есть)
    """
    if details:
        logger.info(f"[USER] User {user_id} {action}: {details}")
    else:
        logger.info(f"[USER] User {user_id} {action}")

def log_system_status(component, status, details=None):
    """
    Логирование статуса системных компонентов
    
    :param component: Название компонента
    :param status: Статус (OK, WARNING, ERROR, etc.)
    :param details: Дополнительные детали (если есть)
    """
    if status == "ERROR":
        log_func = logger.error
    elif status == "WARNING":
        log_func = logger.warning
    else:
        log_func = logger.info
    
    if details:
        log_func(f"[SYSTEM] {component}: {status} - {details}")
    else:
        log_func(f"[SYSTEM] {component}: {status}")

def log_performance(operation, duration_ms, details=None):
    """
    Логирование производительности операций
    
    :param operation: Название операции
    :param duration_ms: Длительность в миллисекундах
    :param details: Дополнительные детали (если есть)
    """
    if details:
        logger.info(f"[PERF] {operation} took {duration_ms}ms - {details}")
    else:
        logger.info(f"[PERF] {operation} took {duration_ms}ms")

def get_logger():
    """
    Получить настроенный логгер
    
    :return: Настроенный логгер
    """
    return logger
