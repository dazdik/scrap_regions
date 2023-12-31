### Скрипт для определения таймзоны и регионов по GeoIP

#### Обзор
Этот скрипт на Python выполняет последовательность HTTP-запросов для определения вашего публичного IP-адреса, нахождения связанной с ним таймзоны и перечисления регионов в этой таймзоне. Процесс включает скрапинг IP-адреса с сайта [2ip.ru](https://2ip.ru/), использование демонстрационной версии MaxMind GeoIP2 для поиска таймзоны и анализ списка регионов и таймзон из Gist пользователя [salkar](https://gist.github.com/salkar/19df1918ee2aed6669e2). Итоговым результатом является файл, перечисляющий обнаруженную таймзону и регионы в ней.

#### Зависимости
Для работы скрипта используются библиотеки `requests` для HTTP-запросов и `python-dotenv` для управления переменными окружения. Для управления этими зависимостями используется `poetry`, инструмент для управления зависимостями и пакетирования в Python.

#### Установка
1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/dazdik/scrap_regions
   cd scrap_regions
   ```

2. **Настройка окружения:**
   - Убедитесь, что у вас установлен `poetry`. Если нет, установите его:
     ```bash
     pip install poetry
     ```
   - Установите зависимости:
     ```bash
     poetry install
     ```

3. **Переменные окружения:**
   - Создайте файл `.env` в корневом каталоге.
   - Добавьте следующие переменные:
     ```
     GEOIP_TOKEN=[Ваш_Token_MaxMind]
     PROXY_URL=[URL_Вашего_Прокси] # Необязательно, используйте, если нужен прокси
     ```

#### Использование
1. **Активация виртуального окружения:**
   ```bash
   poetry shell
   ```

2. **Запуск скрипта:**
   ```bash
   python find_regions.py
   ```

#### Результат
- Скрипт создаст файл `timezone_regions.txt` в директории скрипта.
- В этом файле будет указана таймзона вашего IP-адреса и список регионов в этой таймзоне.

