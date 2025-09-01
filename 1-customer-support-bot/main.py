
### `1-customer-support-bot/main.py`
```python
from transformers import pipeline

# Заглушка для демонстрации
qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

context = "Our support bot helps clients 24/7 by answering common questions."
question = "When can I get help?"

print("User:", question)
print("Bot:", qa(question=question, context=context)["answer"])
