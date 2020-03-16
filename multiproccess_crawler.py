# 1. Однопоточный парсер
# 2. Замер времени
# 3. multiproccessing Pool
# 4. Замер времени
# 5. Экспорт в csv

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.select(".cmc-table--sort-by__rank table td.cmc-table__cell--sort-by__name .cmc-table__column-name")
    links = []

    for div in divs:
        a = div.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    try:
        name = soup.find('h1').text.strip()
    except:
        name =''

    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.strip()
    except:
        price = ''

    data = {'name': name,
            'price': price}

    return data

def write_csv(data):
    with open('coinmarketcap.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)

def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'
    all_links = get_all_links(get_html(url))
    # for index, url in enumerate(all_links):
    #     html = get_html(url)
    #     data = get_page_data(html)
    #     write_csv(data)
    #     print(index)

    with Pool(40) as p:
        p.map(make_all, all_links)

    end = datetime.now()
    total = end-start
    print(str(total))

if __name__ == '__main__':
    main()