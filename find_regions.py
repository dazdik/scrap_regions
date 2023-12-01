import json
import logging
import os
import re
from typing import List, Optional, Tuple

import requests
from dotenv import load_dotenv

load_dotenv()


# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_session_with_proxy() -> requests.Session:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Mobile Safari/537.36"
    }
    proxies = {
        "http": os.getenv("PROXY_URL"),
        "https": os.getenv("PROXY_URL"),
    }
    session.headers.update(headers)
    session.proxies.update(proxies)
    logging.info("Сессия с прокси создана")
    return session


def get_ip_address(session: requests.Session, timeout: int = 5) -> Optional[str]:
    try:
        response = session.get("https://2ip.ru", timeout=timeout)
        ip_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        match = re.search(ip_regex, response.text)
        return match.group() if match else None
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении IP адреса: {e}")
        return None


def get_timezone_by_ip(session: requests.Session, ip_address: str) -> Optional[str]:
    try:
        token = os.getenv("GEOIP_TOKEN")
        session.headers.update({"Authorization": f"Bearer {token}"})
        geoip_url = f"https://geoip.maxmind.com/geoip/v2.1/city/{ip_address}?demo=1"
        response = session.get(geoip_url)

        # Проверяем, не произошла ли ошибка авторизации
        if response.status_code in [400, 401, 403]:
            logging.error(
                f"Ошибка авторизации: Невалидный токен. Код состояния: {response.status_code}"
            )
            return None

        response.raise_for_status()  # Проверка на другие ошибки HTTP

        json_response = response.json()
        return json_response["location"]["time_zone"]
    except requests.RequestException as e:
        logging.error(f"Ошибка сети или HTTP при запросе к API: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка разбора JSON: {e}")
    except KeyError as e:
        logging.error(f"Отсутствующий ключ в JSON ответе: {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")

    return None


def get_regions(session: requests.Session) -> List[Tuple[str, str]]:
    try:
        gist_url = "https://gist.github.com/salkar/19df1918ee2aed6669e2"
        response = session.get(gist_url)
        pattern = re.compile(r"&quot;([^&]+)&quot;,\s*&quot;\s*([^&]+)&quot;")
        return re.findall(pattern, response.text) if response.status_code == 200 else []
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении списка регионов: {e}")
        return []


def filter_regions_by_timezone(
    regions: List[Tuple[str, str]], time_zone: str
) -> List[str]:
    return [region for region, timezone in regions if timezone == time_zone]


def write_to_file(filename: str, time_zone: str, regions: List[str]) -> None:
    with open(filename, "w") as file:
        file.write(f"Таймзона: {time_zone}\n")
        file.write("Регионы:\n")
        for region in regions:
            file.write(region + "\n")
    logging.info(f"Данные записаны в файл {filename}")


def main() -> None:
    session = create_session_with_proxy()
    ip_address = get_ip_address(session)

    if ip_address:
        logging.info(f"Ваш IP-адрес: {ip_address}")
        time_zone = get_timezone_by_ip(session, ip_address)

        if time_zone:
            logging.info(f"Таймзона вашего IP-адреса: {time_zone}")
            regions = get_regions(session)
            filtered_regions = filter_regions_by_timezone(regions, time_zone)
            write_to_file("timezone_regions.txt", time_zone, filtered_regions)
            logging.info("Информация о таймзоне и регионах успешно обработана")
    else:
        print("IP-адрес не найден")


if __name__ == "__main__":
    main()
