import re
from collections import defaultdict

# Загрузка инвертированного индекса
inverted_index = defaultdict(set)

with open("inverted_index.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            lemma = parts[0]
            doc_ids = set(parts[1:])
            inverted_index[lemma] = doc_ids

# Загрузка соответствия id → URL
id_to_url = {}
with open("index.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            doc_id = parts[0]
            url = " ".join(parts[1:])
            id_to_url[doc_id] = url


# Функция для обработки запроса
def evaluate_query(query):
    query = query.lower()

    # Обработка скобок
    while "(" in query:
        start = query.rfind("(")
        end = query.find(")", start)
        if end == -1:
            raise ValueError("Непарные скобки в запросе")
        sub_query = query[start + 1: end]
        sub_result = evaluate_query(sub_query)
        query = query[:start] + " ".join(sorted(sub_result)) + query[end + 1:]

    # Разбиение на токены с учётом операторов
    tokens = re.findall(r'\(|\)|and|or|not|\w+', query)

    stack = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token == "not":
            # Обработка NOT (должен быть перед термином)
            term = tokens[i + 1]
            doc_ids = set(id_to_url.keys()) - inverted_index.get(term, set())
            stack.append(doc_ids)
            i += 2
        elif token in ("and", "or"):
            # Обработка AND/OR (бинарные операторы)
            stack.append(token)
            i += 1
        elif token not in ("(", ")"):
            # Обработка термина
            doc_ids = inverted_index.get(token, set())
            stack.append(doc_ids)
            i += 1
        else:
            i += 1

    # Вычисление результата
    if not stack:
        return set()

    result = stack[0]

    for i in range(1, len(stack), 2):
        if i + 1 >= len(stack):
            break
        operator = stack[i]
        operand = stack[i + 1]

        if operator == "and":
            result &= operand
        elif operator == "or":
            result |= operand

    return result


# Основной цикл поиска
query = input("Введите запрос: ").strip()

try:
    doc_ids = evaluate_query(query)
    print(f"Найдено документов: {len(doc_ids)}")

    for doc_id in sorted(doc_ids):
         print(f"[{doc_id}] {id_to_url.get(doc_id, '?')}")

except Exception as e:
    print(f"Ошибка: {e}")