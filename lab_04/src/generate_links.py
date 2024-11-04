import requests as re
import bs4
import time

FILE_LINKS = "links.txt"
UpToLinks = 100
catalogFormat = "https://www.kedem.ru/recepty-s-foto/{}"
DEBUG = 0

# Множество для хранения уникальных ссылок
unique_links = set()

# выборка ссылок
def fetch_links(page_url):
    global unique_links
    try:
        response = re.get(page_url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        bs = bs4.BeautifulSoup(response.content, "lxml")
        found_links = False  # Флаг для отслеживания найденных ссылок
        # Извлекаем все ссылки на рецепты
        for recipe_block in bs.find_all('div', class_='recipeblock'):
            a_tag = recipe_block.find('a', class_='recipeblocktext')
            if a_tag:
                href = a_tag.get('href')
                if href and "/recipe/" in href:
                    full_link = f"https://www.kedem.ru{href}"  # Формируем полный URL
                    if full_link not in unique_links:  # Проверяем, уникальна ли ссылка
                        if len(unique_links) < UpToLinks:  # Проверяем, меньше ли 50
                            if DEBUG:
                                print(full_link)
                            unique_links.add(full_link)  # Добавляем в множество
                            found_links = True
                        else:
                            return found_links  # Возвращаемся, если достигнут лимит
        # Возвращаем состояние поиска
        return found_links  
    except re.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return False

# Основной цикл для получения ссылок с главной страницы
with open(FILE_LINKS, "w") as f:
    links = 0
    page = 1
    while True:
        if DEBUG:
            print(f"Запрос страницы {page}...")
        try:
            catalogPage = catalogFormat.format(page)
            if fetch_links(catalogPage):
                # Проверяем, достигли ли мы лимита
                if len(unique_links) >= UpToLinks:
                    break
                # Обходим уникальные ссылки
                for link in unique_links.copy():
                    if len(unique_links) >= UpToLinks:
                        break
                    # Выполняем поиск на найденной странице
                    if fetch_links(link):
                        links += 1
            else:
                if DEBUG:
                    print("Ссылки не найдены на странице. Завершение.")
                break
            page += 1
            time.sleep(1)  # Задержка в 1 секунду между запросами

        except re.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            break

    # Сохраняем уникальные ссылки в файл
    for link in unique_links:
        print(link, file=f)

print("Сбор ссылок завершен.")
