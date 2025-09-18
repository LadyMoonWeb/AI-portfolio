# app.py

import streamlit as st
import pandas as pd
from analyzer import extract_audio, transcribe_audio, create_search_index, semantic_search, TEMP_DIR
import os

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(page_title="Video Meeting Analyzer", page_icon="🎥", layout="wide")

st.title("🎥 Video Meeting Analyzer")
st.markdown("Загрузите видеозапись встречи, чтобы получить текстовую расшифровку и возможность поиска по её содержимому.")

# --- Состояние приложения (для хранения данных между действиями) ---
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
    st.session_state.segments_df = None
    st.session_state.search_index = None

# --- ШАГ 1: ЗАГРУЗКА ФАЙЛА ---
st.header("1. Загрузите ваше видео")
uploaded_file = st.file_uploader("Выберите файл (MP4, MOV, AVI)", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # Сохраняем загруженный файл во временную папку
    video_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.video(video_path)

    # --- ШАГ 2: АНАЛИЗ ---
    if st.button("🔍 Проанализировать видео", type="primary"):
        with st.spinner("Пожалуйста, подождите. Идет анализ видео... Это может занять некоторое время."):
            try:
                # 1. Извлечение аудио
                st.write("Шаг 1/4: Извлечение аудио...")
                audio_path = extract_audio(video_path)
                if not audio_path:
                    st.error("Не удалось извлечь аудио из видео.")
                    st.stop()
                
                # 2. Транскрибация
                st.write("Шаг 2/4: Транскрибация речи (модель Whisper)...")
                segments = transcribe_audio(audio_path)
                if not segments:
                    st.error("Транскрибация не дала результатов.")
                    st.stop()
                
                # Сохраняем сегменты в DataFrame для удобства
                st.session_state.segments_df = pd.DataFrame(segments)

                # 3. Создание поискового индекса
                st.write("Шаг 3/4: Создание семантического индекса (FAISS)...")
                st.session_state.search_index = create_search_index(segments)
                
                st.write("Шаг 4/4: Анализ завершен!")
                st.session_state.analysis_complete = True
                st.success("Видео успешно проанализировано! Теперь вы можете искать по содержимому.")

            except Exception as e:
                st.error(f"Произошла ошибка во время анализа: {e}")

# --- ШАГ 3: ПОИСК И ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ ---
if st.session_state.analysis_complete:
    st.header("2. Поиск по содержанию встречи")
    search_query = st.text_input(
        "Что вы хотите найти? (например, 'обсуждение бюджета' или 'кто отвечает за новый проект?')",
        ""
    )

    if search_query:
        results = semantic_search(search_query, st.session_state.search_index, st.session_state.segments_df)
        
        st.subheader("Найденные фрагменты:")
        if not results:
            st.warning("По вашему запросу ничего не найдено.")
        else:
            for res in results:
                st.markdown(f"**🕒 `{res['timestamp']}`** - {res['text']}")
                st.progress(res['similarity'], text=f"Релевантность: {res['similarity']:.2f}")

    # Показываем полную транскрипцию
    with st.expander("Показать полную транскрипцию"):
        full_transcript = " ".join(st.session_state.segments_df['text'])
        st.write(full_transcript)
