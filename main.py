from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from transliterate import translit
import time


# Настройки для Selenium с Firefox
def setup_driver():
    driver_path = "path_to_geckodriver"  # Укажите путь к geckodriver
    driver = webdriver.Firefox()
    return driver


# Поиск и переход на статью в Википедии
def search_wikipedia(driver, query):
    search_url = f"https://ru.wikipedia.org/wiki/{query}"
    driver.get(search_url)
    time.sleep(2)  # Немного ждем, чтобы страница загрузилась полностью
    return driver


# Печать параграфов статьи
def print_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, 'p')
    for i, p in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:\n{p.text}")
        next_step = input("\nПродолжить листать параграфы? (да/нет): ").strip().lower()
        if next_step != 'да':
            break


# Показать связанные статьи с транслитом
def show_related_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, '#bodyContent a')
    valid_links = []

    for link in links:
        href = link.get_attribute('href')
        link_text = link.text

        # Проверяем, что ссылка ведет на другую статью Википедии
        if href and 'wikipedia.org/wiki/' in href:
            # Преобразуем текст ссылки в транслит
            link_translit = translit(link_text, 'ru', reversed=True)
            valid_links.append((href, link_translit))

    # Выводим первые 10 ссылок с транслитом
    for i, (link, link_translit) in enumerate(valid_links[:10]):
        print(f"{i + 1}. {link} ({link_translit})")

    return valid_links


# Основная логика программы
def main():
    driver = setup_driver()

    while True:
        query = input("Введите ваш запрос для поиска на Википедии: ").strip().replace(" ", "_")
        driver = search_wikipedia(driver, query)

        while True:
            print("\nЧто вы хотите сделать дальше?\n")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на связанную страницу")
            print("3. Выйти из программы")

            choice = input("\nВведите номер действия (1/2/3): ").strip()

            if choice == '1':
                print_paragraphs(driver)
            elif choice == '2':
                print("\nСвязанные страницы:")
                links = show_related_links(driver)
                link_choice = int(input("\nВведите номер ссылки, чтобы перейти на новую статью: ").strip()) - 1
                if 0 <= link_choice < len(links):
                    driver.get(links[link_choice][0])  # Переход по выбранной ссылке
                    time.sleep(2)
                    continue
                else:
                    print("Неверный выбор.")
            elif choice == '3':
                print("Выход из программы...")
                driver.quit()
                return
            else:
                print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
