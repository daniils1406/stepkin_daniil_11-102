import requests
from bs4 import BeautifulSoup
import os

# Список страниц для выкачки
urls = [
    "https://habr.com/ru/companies/bothub/news/892496/",
    "https://habr.com/ru/companies/bothub/news/892492/",
    "https://habr.com/ru/news/892488/",
    "https://habr.com/ru/news/892484/",
    "https://habr.com/ru/companies/F6/news/892482/",
    "https://habr.com/ru/articles/892474/",
    "https://habr.com/ru/companies/ruvds/articles/892306/",
    "https://habr.com/ru/articles/892362/",
    "https://habr.com/ru/articles/892372/",
    "https://habr.com/ru/companies/surfstudio/articles/892304/",
    "https://habr.com/ru/companies/airi/articles/891674/",
    "https://habr.com/ru/articles/892302/",
    "https://habr.com/ru/companies/axiomjdk/articles/892230/",
    "https://habr.com/ru/companies/postgrespro/articles/892186/",
    "https://habr.com/ru/companies/aeza/articles/892280/",
    "https://habr.com/ru/companies/timeweb/articles/892288/",
    "https://habr.com/ru/companies/agima/articles/892278/",
    "https://habr.com/ru/companies/skbkontur/articles/891956/",
    "https://habr.com/ru/companies/trinion/articles/892272/",
    "https://habr.com/ru/companies/sibur_official/articles/892264/",
    "https://habr.com/ru/articles/892250/",
    "https://habr.com/ru/articles/892246/",
    "https://habr.com/ru/companies/reksoft/articles/892242/",
    "https://habr.com/ru/articles/892106/",
    "https://habr.com/ru/companies/otus/articles/892240/",
    "https://habr.com/ru/companies/ua-hosting/articles/891818/",
    "https://habr.com/ru/articles/887060/",
    "https://habr.com/ru/companies/alfa/articles/892022/",
    "https://habr.com/ru/companies/selectel/articles/892214/",
    "https://habr.com/ru/articles/892468/",
    "https://habr.com/ru/articles/892460/",
    "https://habr.com/ru/articles/892452/",
    "https://habr.com/ru/articles/892450/",
    "https://habr.com/ru/companies/timeweb/articles/888010/",
    "https://habr.com/ru/articles/892446/",
    "https://habr.com/ru/companies/ruvds/articles/879960/",
    "https://habr.com/ru/companies/otus/articles/892438/",
    "https://habr.com/ru/articles/892418/",
    "https://habr.com/ru/articles/892406/",
    "https://habr.com/ru/articles/892428/",
    "https://habr.com/ru/companies/minerva_media/articles/892426/",
    "https://habr.com/ru/articles/891100/",
    "https://habr.com/ru/articles/892402/",
    "https://habr.com/ru/companies/softonit/articles/892386/",
    "https://habr.com/ru/companies/just_ai/articles/892384/",
    "https://habr.com/ru/articles/892382/",
    "https://habr.com/ru/articles/892378/",
    "https://habr.com/ru/articles/892372/",
    "https://habr.com/ru/articles/892100/",
    "https://habr.com/ru/companies/ruvds/articles/891848/",
    "https://habr.com/ru/companies/habr/articles/892086/",
    "https://habr.com/ru/companies/k2tech/articles/892202/",
    "https://habr.com/ru/articles/892154/",
    "https://habr.com/ru/companies/kryptonite/articles/892164/",
    "https://habr.com/ru/companies/ru_mts/articles/891462/",
    "https://habr.com/ru/articles/892172/",
    "https://habr.com/ru/articles/892174/",
    "https://habr.com/ru/companies/maxilect/articles/892166/",
    "https://habr.com/ru/articles/891924/",
    "https://habr.com/ru/companies/beget/articles/890390/",
    "https://habr.com/ru/companies/sberbank/articles/891376/",
    "https://habr.com/ru/companies/wirenboard/articles/892146/",
    "https://habr.com/ru/companies/inferit/articles/891664/",
    "https://habr.com/ru/articles/892156/",
    "https://habr.com/ru/companies/speach/articles/892150/",
    "https://habr.com/ru/articles/892148/",
    "https://habr.com/ru/articles/891942/",
    "https://habr.com/ru/articles/891942/",
    "https://habr.com/ru/articles/892078/",
    "https://habr.com/ru/articles/892144/",
    "https://habr.com/ru/articles/892142/",
    "https://habr.com/ru/companies/otus/articles/889954/",
    "https://habr.com/ru/articles/892126/",
    "https://habr.com/ru/articles/891972/",
    "https://habr.com/ru/articles/891786/",
    "https://habr.com/ru/articles/892114/",
    "https://habr.com/ru/articles/892108/",
    "https://habr.com/ru/articles/892102/",
    "https://habr.com/ru/companies/otus/articles/892020/",
    "https://habr.com/ru/articles/892088/",
    "https://habr.com/ru/articles/892052/",
    "https://habr.com/ru/articles/892060/",
    "https://habr.com/ru/articles/892068/",
    "https://habr.com/ru/companies/otus/articles/890374/",
    "https://habr.com/ru/articles/859002/",
    "https://habr.com/ru/articles/892048/",
    "https://habr.com/ru/companies/pgk/articles/891496/",
    "https://habr.com/ru/articles/892042/",
    "https://habr.com/ru/articles/888830/",
    "https://habr.com/ru/companies/ncloudtech/articles/890998/",
    "https://habr.com/ru/companies/tbank/articles/891798/",
    "https://habr.com/ru/companies/piter/articles/892036/",
    "https://habr.com/ru/companies/psb/articles/892024/",
    "https://habr.com/ru/articles/892014/",
    "https://habr.com/ru/articles/892008/",
    "https://habr.com/ru/companies/sberbank/articles/891952/",
    "https://habr.com/ru/articles/892000/",
    "https://habr.com/ru/companies/ru_mts/articles/891498/",
    "https://habr.com/ru/companies/t2/articles/891636/",
    "https://habr.com/ru/companies/ringo_mdm/articles/891982/",
    "https://habr.com/ru/companies/habr/articles/891976/"
]

# Создаем папку для сохранения страниц
os.makedirs("pages", exist_ok=True)

index_content = ""

# Обходим каждую страницу
for i, url in enumerate(urls, start=1):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Сохраняем страницу с разметкой
        filename = f"pages/page_{i}.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        # Добавляем в индекс
        index_content += f"{i} {url}\n"
        print(f"Скачано: {url}")

    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")

# Сохраняем index.txt
with open("index.txt", "w", encoding="utf-8") as index_file:
    index_file.write(index_content)

print("Готово! Все страницы сохранены.")
