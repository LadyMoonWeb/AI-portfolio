#  Этот файл нужен, если требуется более сложная логика взаимодействия с OpenAI,
#  которую нельзя реализовать напрямую в n8n.  В простейшем случае, можно обойтись без него.
import openai
import os
from dotenv import load_dotenv

load_dotenv() # загрузка переменных окружения из .env-файла

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt, model="gpt-3.5-turbo"):
  """
  Generates a response from OpenAI's LLM.
  """
  try:
    completion = openai.chat.completions.create(
      model=model,
      messages=[
        {"role": "user", "content": prompt}
      ],
      temperature=0.7,
      max_tokens=150
    )
    return completion.choices[0].message.content
  except Exception as e:
    print(f"Error generating response: {e}")
    return "Произошла ошибка при генерации ответа."

def transcribe_audio(audio_file):
  """
  Transcribes audio file using OpenAI's Whisper API.
  """
  try:
    # TODO: Implement audio transcription
    # response = openai.Audio.transcribe("whisper-1", audio_file)
    # return response["text"]
    return "Транскрибация аудио временно не поддерживается."
  except Exception as e:
    print(f"Error transcribing audio: {e}")
    return "Произошла ошибка при транскрибации аудио."


if __name__ == '__main__':
  # Пример использования (для тестов)
  question = "What is the capital of France?"
  response = generate_response(question)
  print(f"Question: {question}\nResponse: {response}")
