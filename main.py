from os import times, write
import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime
import random
import re



headers = {
    'authority': 'lifemebel.ru',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'dnt': '1',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"Linux"',
    'origin': 'https://lifemebel.ru',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://lifemebel.ru/catalog/stulya/dlya_komnat/kompyuternye/',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'PHPSESSID=DXgixhlGM5dcC4I6edgtOdpUPVGJwGpv; BITRIX_SM_FAV_ITEMS=a%3A0%3A%7B%7D; BITRIX_SM_CITY=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0+%D0%B8+%D0%9C%D0%9E; BITRIX_SM_need_check=1; BITRIX_SM_CITY_KLADR_CODE=7700000000000; BITRIX_SM_FIRST_PAGE_SVET=N; sbjs_migrations=1418474375998%3D1; sbjs_current=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; _ym_uid=1631918777931022062; _ym_d=1631918777; _gcl_au=1.1.1931889815.1631918777; _ga=GA1.2.807592618.1631918777; _gid=GA1.2.188071613.1631918777; _ym_isad=1; _ym_visorc=w; BITRIX_SM_GA_CLIENT_ID=807592618.1631918777; BX_USER_ID=36bdc6039233d579cd830d06ad4cdce1; supportOnlineTalkID=nM6x1WFHTTfGrT1O7g3g5AKOqGLGQBkz; BITRIX_SM_SALE_UID=219281665; BITRIX_SM_VIEWED_ITEMS=a%3A1%3A%7Bi%3A0%3Bs%3A6%3A%22453153%22%3B%7D; BITRIX_SM_LAST_PAGE=%2Fcatalog%2Fstulya%2Fdlya_komnat%2Fkompyuternye%2F; cto_bundle=86xVy19ieXJFUEI5SlQ4ZHlEOVNhbDJwdHBRN0E5ZEpUVXJ2TjI0ekJUV3dLbGNheTlkSDFGTFI1TFElMkZYOWFPeFRsUTRqRVBKNjBKU28wdTc2S2lqWHZCWXJMNDlaM2RLMHdwc05JZldSUVh2aVFOZ0JPcVpNc3J6WVZlWGlXUmlZNzJORTJ2SEtwc3haQmZrR3lINWVXOEh0dyUzRCUzRA; 19379.vst=%7B%22s%22%3A%22a8b86907-555b-46ae-9d41-4ddee44b3ad8%22%2C%22t%22%3A%22new%22%2C%22lu%22%3A1631920401396%2C%22lv%22%3A1631918780063%2C%22lp%22%3A0%7D; _gat_UA-2615708-4=1',
}

# data = {
#   'AJAX': 'Y',
#   'noind': 'Y',
#   'SECTION_ID': '51',
#   'NUM_SIZE': '48',
#   'PAGEN_1': '45',
#   'NEXT_PAGE': 'N',
#   'sort_by': 'sort'
# }


"""
Собираю данные с сайта по продаже кресел
В первой функции, соберу все ссылки на карточки с креслами
Во второй функции, буду заходить в карточки и брать данные
Название, новый прайс, старый прайс, ширину кресла, высота кресла, вес, механихзм качания, 
максимальная нагрузка, ссылку на изображение, ссылку на карточку.
Запишу в csv, json.
"""


def index_chairs():
    response = requests.get('https://lifemebel.ru/catalog/stulya/dlya_komnat/kompyuternye/page_44/', headers=headers)
        
    # сохранил странцу
    with open('index_chairs.html', 'w') as file:
        file.write(response.text)

    # читаю страницу в фаил
    with open('index_chairs.html') as file:
        src = file.read()  
        
    # создаю обьект BeautifulSoup
    soup = BeautifulSoup(src, 'lxml')
    
    # нахожу последнюю страницу
    last_page = int(soup.find('div', class_='pagination-list-wrapper').find_all('li')[-1].text)
    
    # в эту переменную буду записывать ссылки на страницу
    urls_list = []
    
    # генератор ссылок на каждую старницу
    for pagination_page_count in range (1, 3): #(1, last_page + 1)       
        pagination_page_url = f"https://lifemebel.ru/catalog/stulya/dlya_komnat/kompyuternye/page_{pagination_page_count}/"
        print(f'[info] Собираю ссылки с {pagination_page_count} из {last_page} страниц')
        
        # делаю запрос к каждой странице
        r = requests.get(url=pagination_page_url, headers=headers)
        
        # делаю паузу между запросами
        time.sleep(random.randrange(2, 4))
        
        soup = BeautifulSoup(r.text, 'lxml')  
    
        # общий блок с сылками на карточки
        all_card_link = soup.find('div', class_='catalog-products').find_all('div', class_='catalog-product-title')
       
        # в блоке нахожу ссылки на карточки    
        for i in all_card_link:
            link_card = f"https://lifemebel.ru/{i.find('a').get('href')}"
            
            # упаковываю ссылки в переменную
            urls_list.append(link_card)
            
    # записываю посторочно ссылки в фаил urls_list
    with open(f'urls_list.txt', 'a') as file:
        for line in urls_list:
            file.write(f'{line}\n')
                
    print('[info] Сбор ссылок на страницы закончен')
    
    return urls_list


"""
Во второй функции, буду заходить в карточки и брать данные
Название, новый прайс, старый прайс, ширину кресла, высота кресла, вес, 
механихзм качания, максимальная нагрузка, ссылку на изображение, ссылку на карточку
"""

def collect_data_chairs(urls_list):
    
    # для мониторинга сбора данных по каждому креслу
    # общее количество кресел
    urls_count = len(urls_list)
    
    # после обработки каждого кресла буду увеличивать на 1
    count = 1  
    
    # шаблон для записи в csv
    with open('data_chairs.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название кресла',
                'Старая цена',
                'Новая цена',
                'Ширина',
                'Высота кресла',
                'Вес',
                'Максимальная нагрузка',
                'Механизм качания',
                'Ссылка на карточку'
            )
        )
        
    # переменная для записи в json
    all_data_chairs = []        
    
    # читаю ссылки из списка
    for url in urls_list[:3]:       
    
        print(f'Обработал {count} из {urls_count} кресел')        
        
        # делаю запрос к каждой карточке
        response = requests.get(url=url, headers=headers)
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # попробую сохранить страницу чтoбы найти там строку с новой ценой
        with open('card_index_new_price.html', 'w') as file:
            file.write(response.text)
        
        try:    
            #  название кресла
            card_name = soup.find('div', class_='new-product-title').find('h2').text.replace('\n', '')        
        except Exception as ex:
            card_name = None
            
        try:
            # Старая цена        
            card_old_price = soup.find('div', class_='new-product-price').text.replace('\n', '')
        except Exception as ex:
            card_old_price = None
            
        try:
            # Новая цена ПРОБЛЕМА!!!!!
            # card_new_price = soup.find('div', class_='container')
            card_new_price = 'ПРОБЛЕМА!!!!!'
            
        except Exception as ex:
            card_new_price = None
            
        try:
            # Ширина
            card_width = soup.find('td', text=re.compile('Ширина кресла')).find_next().text.replace('\n', '')
        except Exception as ex:
            card_width = None
        
        try:
            # Высота кресла
            card_height = soup.find('td', text=re.compile('Высота кресла')).find_next().text.replace('\n', '')
        except Exception as ex:
            card_height = None
            
        try:
            # Вес
            card_weight = soup.find('td', text=re.compile('Вес')).find_next().text.replace('\n', '')
        except Exception as ex:
            card_weight = None
            
        try:
            # Максимальная нагрузка
            card_max_weight = soup.find('td', text=re.compile('Максимальная нагрузка на газпатрон')).find_next().text.replace('\n', '')
        except Exception as ex:
            card_max_weight = None
            
        try:
            # Механизм качания
            card_swing_mechanizm = soup.find('td', text=re.compile('Механизм качания')).find_next().text.replace('\n', '')
        except Exception as ex:
            card_swing_mechanizm = None
               
        # Ссылка на карточку
        card_link = url
        
        # Упаковываю данные в csv
        with open('data_chairs.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    card_name,
                    card_old_price,
                    card_new_price,
                    card_width,
                    card_height,
                    card_max_weight,
                    card_weight,
                    card_max_weight,
                    card_swing_mechanizm,
                    card_link
                )
            )
            
        # упаковываю данные для записи в json
        all_data_chairs.append(
            {
                'card_name': card_name,
                'card_old_price': card_old_price,
                'card_new_price': card_new_price,
                'card_width': card_width,
                'card_height': card_height,
                'card_max_weight': card_max_weight,
                'card_swing_mechanizm': card_swing_mechanizm,
                'card_link': card_link                
            }
        )
        
        # пауза после каждого кресла
        time.sleep(random.randrange(2, 4))  
        
        # после обработки каждого кресла буду увеличивать на 1
        count += 1     
        
        print(f"Название кресла: {card_name}\nСтарая цена: {card_old_price}\nНовая цена: может попробовать сохранить страницу и там покопаться\nШирина кресла: {card_width}\nВысота кресла: {card_height}\nВес: {card_weight}\nМаксимальная нагрузка: {card_max_weight}\nМеханизм качания: {card_swing_mechanizm}\n -*-*-*-*-*-*-*\nСсылка на карточку: {card_link}\n")
        
    # запишу json
    with open('all_data_chairs.json', 'w') as file:
        json.dump(all_data_chairs, file, indent=4, ensure_ascii=False)
      
    print('[info] Сбор данных по креслам завершен')
    return 'Сбор данных завершен'
        
            


def main():
    
    # время старта кода
    start_time = time.time()
    print(f'Время старта кода: {datetime.fromtimestamp(start_time)}\n')
    
    # активирую функцию сбора инфрмации из карточек, а она в свою очередь запускает функцию сбора ссылок на карточки
    collect_data_chairs(index_chairs())    

    # время окончания работы кода
    finish_time = time.time()
    print(f'Время окончания работы кода: {datetime.fromtimestamp(finish_time)}\n')
    
    # вычислил время работы кода
    working_time = finish_time - start_time
    print(f'Время работы кода: {working_time/60} мин.')
    
"""
мне не нравится:
    вывод времени работы кода:
    Время старта кода: 2021-09-20 18:21:26.308046 
    Время окончания работы кода: 2021-09-20 18:21:36.476111
    Время работы кода: 0.1694677432378133 мин.
Я не могу вывести новую цену, ее нет в коде т.к. нет в html коде, кроме json какой то..
"""
    

# test commit for git

if __name__ == '__main__':
    main()
    