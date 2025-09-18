# analyzer.py

import os
import whisper
import ffmpeg
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

# --- КОНСТАНТЫ ---
TEMP_DIR = "temp"
AUDIO_FILENAME = os.path.join(TEMP_DIR, "extracted_audio.wav")

# Убедимся, что папка для временных файлов существует
os.makedirs(TEMP_DIR, exist_ok=True)

# --- ИНИЦИАЛИЗАЦИЯ МОДЕЛЕЙ (выполняется один раз при запуске) ---
print("Загрузка моделей...")
# Выбираем модель Whisper. 'base' - быстрая, 'medium' - более точная.
transcriber_model = whisper.load_model("base")
# Модель для создания векторных представлений текста
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Модели успешно загружены.")


def extract_audio(video_path):
    """Извлекает аудиодорожку из видеофайла и сохраняет ее."""
    try:
        print(f"Извлечение аудио из {video_path}...")
        (
            ffmpeg
            .input(video_path)
            .output(AUDIO_FILENAME, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"Аудио успешно сохранено в {AUDIO_FILENAME}")
        return AUDIO_FILENAME
    except ffmpeg.Error as e:
        print("Ошибка ffmpeg:", e.stderr.decode())
        return None

def transcribe_audio(audio_path):
    """Транскрибирует аудиофайл с помощью Whisper, возвращая сегменты с таймкодами."""
    print("Начало транскрибации...")
    result = transcriber_model.transcribe(audio_path, verbose=False)
    print("Транскрибация завершена.")
    return result['segments']

def create_search_index(segments):
    """Создает векторный индекс FAISS на основе текстовых сегментов."""
    print("Создание семантического индекса...")
    texts = [segment['text'] for segment in segments]
    
    # Преобразуем текст в векторы (эмбеддинги)
    embeddings = embedding_model.encode(texts, convert_to_tensor=True).cpu().numpy()
    
    # Нормализуем векторы для косинусного сходства
    faiss.normalize_L2(embeddings)
    
    # Создаем индекс FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension) # IP = Inner Product, эквивалентно косинусному сходству для L2-норм векторов
    index.add(embeddings)
    
    print("Индекс успешно создан.")
    return index

def semantic_search(query, index, segments_df, top_k=5):
    """Выполняет семантический поиск по индексу FAISS."""
    print(f"Выполнение поиска по запросу: '{query}'")
    
    # Кодируем поисковый запрос в вектор
    query_embedding = embedding_model.encode([query], convert_to_tensor=True).cpu().numpy()
    faiss.normalize_L2(query_embedding)
    
    # Ищем K ближайших соседей
    distances, indices = index.search(query_embedding, top_k)
    
    # Собираем результаты
    results = []
    for i in range(top_k):
        idx = indices[0][i]
        result_segment = segments_df.iloc[idx]
        
        # Преобразуем секунды в формат MM:SS
        start_time = int(result_segment['start'])
        minutes = start_time // 60
        seconds = start_time % 60
        
        results.append({
            'timestamp': f"{minutes:02d}:{seconds:02d}",
            'text': result_segment['text'],
            'similarity': distances[0][i]
        })
        
    return results
