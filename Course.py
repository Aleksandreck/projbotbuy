import requests
import xml.etree.ElementTree as ET
import math

def get_cny_to_rub_rate():
    # URL Центробанка для получения курсов
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    
    # Отправляем запрос
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Ошибка при получении данных от Центробанка")
    
    # Парсим XML
    tree = ET.fromstring(response.content)
    
    # Ищем курс для юаня (код валюты: CNY)
    for currency in tree.findall("Valute"):
        if currency.find("CharCode").text == "CNY":
            rate = currency.find("Value").text.replace(",", ".")
            return float(rate)
    
    raise Exception("Курс юаня не найден")


def GetCoast(n):
    sumr = ((n + 50) * (get_cny_to_rub_rate() + 1)) * 1.05 + 2000
    sumr_rounded = math.ceil(sumr * 100) / 100  # Умножаем на 100, округляем вверх, затем делим обратно
    return sumr_rounded

