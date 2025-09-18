import os
import sys
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

# Загрузка и извлечение текста из PDF
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Индексация текста с помощью FAISS
def create_faiss_index(text, index_path):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    vectorstore.save_local(index_path)
    return vectorstore

# Загрузка индекса
def load_faiss_index(index_path):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(index_path, embeddings)

# Ответ на вопросы
def answer_question(vectorstore, question):
    llm = OpenAI(model_name="gpt-4", temperature=0)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = vectorstore.similarity_search(question)
    answer = chain.run(input_documents=docs, question=question)
    return answer

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Document Q&A Bot")
    parser.add_argument("command", choices=["index", "ask"], help="index — создать индекс, ask — задать вопрос")
    parser.add_argument("--file", help="Путь к PDF файлу")
    parser.add_argument("--index", default="faiss_index", help="Папка для индекса")
    parser.add_argument("--question", help="Вопрос к документу")

    args = parser.parse_args()

    if args.command == "index":
        if not args.file:
            print("Ошибка: укажите PDF файл через --file")
            sys.exit(1)
        text = load_pdf(args.file)
        print("Создаем индекс...")
        create_faiss_index(text, args.index)
        print("Индекс создан и сохранен в", args.index)

    elif args.command == "ask":
        if not args.question:
            print("Ошибка: укажите вопрос через --question")
            sys.exit(1)
        if not os.path.exists(args.index):
            print(f"Индекс {args.index} не найден. Сначала создайте индекс с помощью команды: index")
            sys.exit(1)
        vectorstore = load_faiss_index(args.index)
        answer = answer_question(vectorstore, args.question)
        print("Ответ:", answer)
