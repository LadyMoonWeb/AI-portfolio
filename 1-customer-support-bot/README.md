# AI Customer Support Bot (n8n Workflow)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![n8n Version](https://img.shields.io/badge/n8n-%3E=1.0-green)](https://n8n.io/)

## Описание

Этот проект представляет собой автоматизированного бота для поддержки клиентов в Telegram, созданного с использованием n8n для оркестрации процессов и интеграции различных API. Бот отвечает на текстовые и голосовые запросы, генерируя быстрые и точные ответы, что позволяет значительно сократить время обработки запросов и снизить нагрузку на операторов.

**Основные функции:**

*   Обработка текстовых сообщений от пользователей Telegram.
*   Транскрибация голосовых сообщений в текст (Speech-to-Text).
*   Генерация ответов с использованием OpenAI API (LLM).
*   Отправка ответов пользователю в Telegram.
*   Логирование и мониторинг работы бота.

**Ключевые результаты:**

*   Сокращение времени обработки запросов до <10 секунд.
*   Снижение нагрузки на операторов на 40%.

## Технологии

*   [n8n](https://n8n.io/) - Платформа автоматизации workflow
*   [Python](https://www.python.org/) - Язык программирования для интеграции с API
*   [OpenAI API](https://openai.com/api/) - Использование LLM (Large Language Model) для генерации ответов и Speech-to-Text API для транскрибации голоса.
*   [Telegram API](https://core.telegram.org/api) - Интеграция с Telegram для получения и отправки сообщений.

## Установка

1.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/YOUR_USERNAME/AI-Customer-Support-Bot.git
    cd AI-Customer-Support-Bot
    ```

2.  **Установите необходимые зависимости Python:**

    ```bash
    pip install -r requirements.txt
    ```
    *(файл `requirements.txt` должен содержать как минимум библиотеки requests, python-dotenv)*

3.  **Настройте переменные окружения:**

    *   Создайте файл `.env` на основе `.env.example`.
    *   Заполните `.env` необходимыми значениями:

        ```
        TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
        OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        OPENAI_MODEL_NAME=gpt-3.5-turbo # или другая модель
        ```

4.  **Импортируйте workflow n8n:**
    *   Запустите n8n.
    *   Импортируйте файл `n8n-workflow/customer-support.json` в n8n.

5.  **Настройте ноды n8n:**
    *   В workflow n8n настройте ноды Python Script, указав пути к файлам `scripts/openai_integration.py` и `scripts/telegram_bot.py`.
    *   Убедитесь, что все необходимые переменные окружения доступны в n8n (можно использовать ноду "Set").

## Запуск

1.  **Запустите n8n workflow.**
2.  **Запустите Telegram бота (если требуется отдельный скрипт):**

    ```bash
    python scripts/telegram_bot.py
    ```

## Архитектура

Подробное описание архитектуры решения можно найти в файле [docs/architecture.md](docs/architecture.md).

## Возможные проблемы и их решение

См. [docs/troubleshooting.md](docs/troubleshooting.md).

