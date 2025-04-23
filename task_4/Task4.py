import os
import math
import re
from collections import defaultdict, Counter
from bs4 import BeautifulSoup

# ---------- Загрузка токенов и лемм ----------
with open("tokens.txt", encoding="utf-8") as f:
    token_list = set(line.strip() for line in f if line.strip())

with open("lemmas.txt", encoding="utf-8") as f:
    lemma_to_tokens = {}
    token_to_lemma = {}
    for line in f:
        parts = line.strip().split()
        if not parts:
            continue
        lemma, *tokens = parts
        lemma_to_tokens[lemma] = set(tokens)
        for token in tokens:
            token_to_lemma[token] = lemma

# ---------- Подготовка ----------
doc_dir = "pages"
term_doc_freq = defaultdict(int)
lemma_doc_freq = defaultdict(int)
all_docs_tokens = []
filenames = sorted(os.listdir(doc_dir))

# ---------- Обработка документов: TF + сбор df ----------
for filename in filenames:
    path = os.path.join(doc_dir, filename)
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        text = soup.get_text().lower()

    words = re.findall(r"\b[a-zа-яё]+\b", text)
    tokens = [w for w in words if w in token_list]
    all_docs_tokens.append(tokens)

    unique_terms = set(tokens)
    for term in unique_terms:
        term_doc_freq[term] += 1

    lemma_counts = set()
    for token in unique_terms:
        lemma = token_to_lemma.get(token)
        if lemma:
            lemma_counts.add(lemma)
    for lemma in lemma_counts:
        lemma_doc_freq[lemma] += 1

# ---------- Расчёт IDF ----------
N = len(all_docs_tokens)
term_idf = {term: math.log(N / (1 + df)) for term, df in term_doc_freq.items()}
lemma_idf = {lemma: math.log(N / (1 + df)) for lemma, df in lemma_doc_freq.items()}

# ---------- Создание папок ----------
os.makedirs("tfidf_terms", exist_ok=True)
os.makedirs("tfidf_lemmas", exist_ok=True)

# ---------- Вычисление TF-IDF по токенам и леммам ----------
for i, tokens in enumerate(all_docs_tokens, start=1):
    term_counts = Counter(tokens)
    total_terms = len(tokens)

    # TF-IDF по терминам
    term_tfidf_lines = []
    for term, count in term_counts.items():
        tf = count / total_terms
        idf = term_idf.get(term, 0)
        tfidf = tf * idf
        term_tfidf_lines.append(f"{term} {idf:.6f} {tfidf:.6f}")

    with open(f"tfidf_terms/tfidf_terms_doc_{i}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(term_tfidf_lines))

    # TF-IDF по леммам
    lemma_counts = defaultdict(int)
    for token in tokens:
        lemma = token_to_lemma.get(token)
        if lemma:
            lemma_counts[lemma] += 1

    lemma_tfidf_lines = []
    for lemma, count in lemma_counts.items():
        tf = count / total_terms
        idf = lemma_idf.get(lemma, 0)
        tfidf = tf * idf
        lemma_tfidf_lines.append(f"{lemma} {idf:.6f} {tfidf:.6f}")

    with open(f"tfidf_lemmas/tfidf_lemmas_doc_{i}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lemma_tfidf_lines))
