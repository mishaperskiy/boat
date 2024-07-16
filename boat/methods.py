import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs


def normmetod(cur, maney, tip):
    url = 'https://garantex.org/trading/btcrub'
    request = requests.get(url)
    start = request.text.find("window.gon = ")
    end = request.text[start:].find(";")
    kal_iz_zhopy = request.text[start + len("window.gon = "):][:end - len("window.gon = ")]
    norm = json.loads(kal_iz_zhopy)
    key = cur.lower() + 'rub'
    res = float(norm['exchangers'][key]['bid'][0]['price'])
    if tip == 'buy':
        return float(0.98*maney/res)
    else:
        return float(maney*res*0.98)


def coolmetod(cur, maney, tip):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if cur == 'TRX':
        url = 'https://bits.media/converter/trx/usdt/'
        key = 'Tron'
    else:
        url = 'https://bits.media/converter/xmr/usdt/'
        key = 'Monero'
    wd = webdriver.Chrome(options= chrome_options)
    wd.get(url)
    html = wd.page_source
    soup = bs(html, "html.parser")
    cur_str = soup.find('div', class_='row crypto_curr_link_block crypto_calc_link_block mb-20'). \
         find('td', string=key).find_next_sibling('td').text
    cur_float = float(cur_str.replace(' ', ''))
    wd.close()
    if tip == 'buy':
        return float(0.98*maney/cur_float)
    else:
        return float(maney * cur_float * 0.98)


