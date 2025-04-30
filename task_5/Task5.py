import os
import math
import re
from collections import defaultdict, Counter

def load_index(directory):
    index = {}
    for fname in os.listdir(directory):
        doc_id = int(fname.split("_")[-1].split(".")[0])
        index[doc_id] = {}
        with open(os.path.join(directory, fname), encoding="utf-8") as f:
            for line in f:
                lemma, idf, tfidf = line.strip().split()
                index[doc_id][lemma] = float(tfidf)
    return index

# Загрузка index.txt (номер -> ссылка)
def load_doc_links():
    links = {}
    with open("index.txt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                links[int(parts[0])] = parts[1]
    return links

# Токенизация + очистка
def tokenize(text):
    text = text.lower()
    return re.findall(r"\b[а-яa-zё]+\b", text)

# Загрузка лемм
def load_lemmas():
    token_to_lemma = {}
    with open("lemmas.txt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            lemma, *tokens = parts
            for token in tokens:
                token_to_lemma[token] = lemma
    return token_to_lemma

# Построение вектора запроса
def vectorize_query(query, token_to_lemma, doc_index):
    tokens = tokenize(query)
    lemmas = [token_to_lemma.get(token) for token in tokens if token in token_to_lemma]
    lemmas = [lemma for lemma in lemmas if lemma is not None]

    query_tf = Counter(lemmas)
    total = sum(query_tf.values())

    query_vector = {}
    for lemma, count in query_tf.items():
        tf = count / total
        # Берем IDF из любого документа (они одинаковые)
        idf = next((doc.get(lemma, 0) / tf for doc in doc_index.values() if lemma in doc), 0)
        query_vector[lemma] = tf * idf
    return query_vector

# Косинусное сходство
def cosine_similarity(vec1, vec2):
    dot_product = sum(vec1[k] * vec2.get(k, 0) for k in vec1)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

# Поиск
def search(query, top_k=5):
    token_to_lemma = load_lemmas()
    doc_links = load_doc_links()
    doc_index = load_index("tfidf_lemmas")

    query_vector = vectorize_query(query, token_to_lemma, doc_index)

    results = []
    for doc_id, doc_vector in doc_index.items():
        score = cosine_similarity(query_vector, doc_vector)
        if score > 0:
            results.append((score, doc_id))

    results.sort(reverse=True)
    print("\n🔍 Топ результатов по запросу:", query)
    for score, doc_id in results[:top_k]:
        print(f"[{score:.4f}] Документ {doc_id}: {doc_links.get(doc_id)}")

#  Использование
if __name__ == "__main__":
    while True:
        q = input("\nВведите поисковый запрос (или 'exit'): ").strip()
        if q.lower() == "exit":
            break
        search(q)
