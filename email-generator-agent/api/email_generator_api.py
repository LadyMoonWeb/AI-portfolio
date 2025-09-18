# api/email_generator_api.py

import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения (OPENAI_API_KEY) из .env файла
load_dotenv()

# --- ИНИЦИАЛИЗАЦИЯ ---
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    raise ValueError("OPENAI_API_KEY не найден. Убедитесь, что он задан в .env файле.")

# --- АЛГОРИТМ: СБОРКА ПРОМПТА ---
def build_prompt(customer_data):
    """
    Собирает детализированный промпт для GPT на основе данных о клиенте.
    Это сердце нашего AI-агента. Чем лучше промпт, тем лучше результат.
    """
    # Извлекаем данные с проверкой на их наличие
    name = customer_data.get("name", "клиент")
    company = customer_data.get("company", "ваша компания")
    position = customer_data.get("position", "специалист")
    interest = customer_data.get("interest", "повышение эффективности")
    product = "наш сервис по автоматизации бизнес-процессов"

    prompt = f"""
    Ты - первоклассный менеджер по продажам по имени Алекс. Твой стиль общения - дружелюбный, но профессиональный.
    Твоя задача - написать короткое, персонализированное письмо для потенциального клиента.

    Цель письма: заинтересовать клиента и предложить короткий 15-минутный звонок для обсуждения деталей.
    
    Вот информация о клиенте:
    - Имя: {name}
    - Компания: {company}
    - Должность: {position}
    - Сфера интересов/проблема: {interest}

    Вот информация о продукте, который ты предлагаешь:
    - Продукт: {product}

    Правила для генерации письма:
    1.  Обращайся к клиенту по имени.
    2.  В первом абзаце покажи, что ты изучил информацию о клиенте. Свяжи его должность или сферу интересов с пользой от твоего продукта.
    3.  Не используй банальные фразы вроде "надеюсь, это письмо застало вас в добром здравии".
    4.  Письмо должно быть коротким (не более 150 слов).
    5.  В конце обязательно должен быть четкий призыв к действию (call to action) - предложение созвониться.
    6.  Тема письма должна быть интригующей и короткой.
    
    Сгенерируй ответ в формате JSON с двумя ключами: "subject" для темы письма и "body" для текста письма.
    """
    return prompt


# --- API ЭНДПОИНТ ---
@app.route('/generate-email', methods=['POST'])
def generate_email():
    """
    API-эндпоинт, который принимает данные о клиенте и возвращает сгенерированное письмо.
    """
    # Получаем JSON данные из запроса от n8n
    customer_data = request.json
    if not customer_data:
        return jsonify({"error": "Request body must be a valid JSON"}), 400

    print(f"Получены данные для генерации: {customer_data}")
    
    try:
        # 1. Строим промпт
        prompt = build_prompt(customer_data)

        # 2. Вызываем API OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o",  # Рекомендуется использовать более новую и мощную модель
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Ты полезный ассистент, который возвращает результат в формате JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # 3. Парсим и возвращаем результат
        generated_email = completion.choices[0].message.content
        print(f"Сгенерированный ответ от OpenAI: {generated_email}")
        
        # Возвращаем JSON, который пришел от OpenAI, напрямую
        return generated_email, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return jsonify({"error": str(e)}), 500

# --- ЗАПУСК СЕРВЕРА ---
if __name__ == '__main__':
    # Для локального запуска используйте `flask run` в терминале
    app.run(debug=True)
