import os
import re
from bs4 import BeautifulSoup
from pymorphy2 import MorphAnalyzer
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt_tab')
nltk.download("punkt")
nltk.download("stopwords")


import inspect
from collections import namedtuple

if not hasattr(inspect, 'getargspec'):
    from inspect import signature, Parameter

    ArgSpec = namedtuple('ArgSpec', ['args', 'varargs', 'keywords', 'defaults'])

    def getargspec(func):
        sig = signature(func)
        args = []
        varargs = None
        keywords = None
        defaults = []

        for name, param in sig.parameters.items():
            if param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
                args.append(name)
                if param.default is not Parameter.empty:
                    defaults.append(param.default)
            elif param.kind == Parameter.VAR_POSITIONAL:
                varargs = name
            elif param.kind == Parameter.VAR_KEYWORD:
                keywords = name

        defaults = tuple(defaults) if defaults else None
        return ArgSpec(args, varargs, keywords, defaults)

    inspect.getargspec = getargspec



# Папка с HTML-файлами
FOLDER = "pages"
FILES = [os.path.join(FOLDER, f) for f in os.listdir(FOLDER) if f.endswith(".html")]

# Инициализация
morph = MorphAnalyzer()
russian_stopwords = set(stopwords.words("russian"))

# Регулярка для нормальных слов: только буквы
word_pattern = re.compile("^[а-яА-ЯёЁ]+$")

tokens_set = set()

# --- ЭТАП 1: Токенизация ---
for filepath in FILES:
    with open(filepath, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        text = soup.get_text()

    words = word_tokenize(text.lower())

    for word in words:
        if word_pattern.match(word) and word not in russian_stopwords:
            tokens_set.add(word)

# Сортируем для читаемости
tokens_list = sorted(tokens_set)

# Сохраняем список токенов
with open("tokens.txt", "w", encoding="utf-8") as f:
    for token in tokens_list:
        f.write(token + "\n")

# --- ЭТАП 2: Лемматизация ---
lemma_dict = defaultdict(set)

for token in tokens_list:
    lemma = morph.parse(token)[0].normal_form
    lemma_dict[lemma].add(token)

# Сохраняем результат
with open("lemmas.txt", "w", encoding="utf-8") as f:
    for lemma in sorted(lemma_dict.keys()):
        line = lemma + " " + " ".join(sorted(lemma_dict[lemma]))
        f.write(line + "\n")

print("Готово! Созданы файлы tokens.txt и lemmas.txt.")
