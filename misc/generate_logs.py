from datetime import datetime
from random import choice, randint, seed

# Настройки "ручек" API
API_ENDPOINTS = [
    "/api/users/",
    "/api/products/",
    "/api/orders/",
    "/api/auth/login/",
    "/api/payments/"
]

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
STATUS_CODES = [200] * 10 + [201, 400, 401, 403, 404, 500]
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def generate_log_entry():
    """Генерирует одну запись лога для API ручки"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    method = choice(HTTP_METHODS)
    endpoint = choice(API_ENDPOINTS)
    status = choice(STATUS_CODES)
    duration = f"{randint(10, 500) / 1000:.3f}"

    # Определяем уровень логирования на основе статуса
    level = ""
    if status == 500:
        level = "CRITICAL"
    elif status >= 400:
        level = 'ERROR'
    elif status > 200:
        level = "WARNING"
    else:
        level = choice(["DEBUG", "INFO"])

    message = f"{method} {endpoint} {status} {duration}s"

    if level in ["ERROR", "CRITICAL"]:
        error_msg = choice([
            "Internal server error",
            "Database connection failed",
            "Invalid request data",
            "Permission denied"
        ])
        message += f"\nError: {error_msg}"

    return f"{timestamp} [{level}] django.request: {message}"


def write_logs_to_file(filename, num_entries=100):
    """Генерирует и записывает логи в файл"""
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(num_entries):
            log_entry = generate_log_entry()
            f.write(log_entry + "\n")


if __name__ == "__main__":
    seed(123)
    # Короткий файл с логами
    short_log = "../src/short_django_api.log"
    write_logs_to_file(short_log, 50)
    print(f"Сгенерировано 50 записей логов в файл {short_log}")

    # Крупный файл с логами
    big_log = "../src/big_django_api.log"
    write_logs_to_file(big_log, 10 ** 5)
    print(f"Сгенерировано {10 ** 5} записей логов в файл {big_log}")
