import os
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Загрузка стоп-слов и инициализация морфологического анализатора
russian_stopwords = set(stopwords.words("russian"))
morph = MorphAnalyzer()
word_pattern = re.compile("^[а-яё]+$")

# Чтение index.txt для получения соответствия id → URL
id_to_url = {}
with open("index.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            doc_id = parts[0]
            url = " ".join(parts[1:])
            id_to_url[doc_id] = url

# Построение инвертированного индекса
inverted_index = {}

for doc_id in id_to_url:
    filepath = os.path.join("pages", f"page_{doc_id}.html")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            article_body = soup.find("div", class_="tm-article-body")
            text = article_body.get_text(separator=" ") if article_body else soup.get_text(separator=" ")

            words = word_tokenize(text.lower())

            for word in words:
                if (
                        word_pattern.match(word)
                        and word not in russian_stopwords
                        and 2 <= len(word) <= 20
                ):
                    lemma = morph.parse(word)[0].normal_form
                    if lemma not in inverted_index:
                        inverted_index[lemma] = set()
                    inverted_index[lemma].add(doc_id)

    except Exception as e:
        print(f"Ошибка обработки документа {doc_id}: {e}")

# Сохранение инвертированного индекса
with open("inverted_index.txt", "w", encoding="utf-8") as f:
    for lemma in sorted(inverted_index.keys()):
        doc_ids = " ".join(sorted(inverted_index[lemma]))
        f.write(f"{lemma} {doc_ids}\n")

print("Инвертированный индекс сохранён в inverted_index.txt")