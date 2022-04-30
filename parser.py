from itertools import count
from random import random
import string
import requests
import config
import requests
from sqlite import sqlight
from bs4 import BeautifulSoup
import schedule
import time
import asyncio

url = 'https://coinmarketcap.com/'

db = sqlight('crypto_coins.db')

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

##Here we are getting html file from page's url, which variable called "url"
def get_html_for_url(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    res = r.text
    return res

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
##Here we are getting page count by simply searching the last "li" with class "page". Later we will use this information by adding page attribute to every page url
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li', class_='page')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
##Here we are getting a list with all urls heading to currencies overview
def get_url(html, url_mn):
    soup = BeautifulSoup(html, 'html.parser')
    links1 = soup.find_all('tr', class_='sc-1rqmhtg-0 jUUSMS')
    links2 = soup.find_all('div', class_='sc-16r8icm-0 escjiH')
    url_list = []
    for item in links2:
        url2 = item.find('a', class_='cmc-link')['href']
        final_url = url_mn + url2
        url_list.append(final_url)
    for item in links1:
        url2 = item.find('a', class_='cmc-link')['href']
        final_url = url_mn + url2
        url_list.append(final_url)
    return url_list
## This function just locates every variable
def get_content(list):
    coins = []
    for link in list[:5]:
        time.sleep(2)
        html = get_html_for_url(link)
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('div', class_='sc-16r8icm-0 kjciSH priceTitle').find('span').get_text() != None:
            price = soup.find('div', class_='sc-16r8icm-0 kjciSH priceTitle').find('span').get_text()
        ticket = soup.find('small', class_='nameSymbol').get_text()
        coin_name = soup.find('h2', class_='sc-1q9q90x-0 jCInrl h1').get_text().replace(ticket, '', 1)
        percent = soup.find('div', class_='sc-16r8icm-0 kjciSH priceTitle').get_text().replace(price, '')
        print(coin_name)
        arrow1 = soup.find('span', class_='sc-15yy2pl-0 gEePkg')
        plus = ''
        if arrow1 == None:
            arrow = soup.find('span', class_='sc-15yy2pl-0 feeyND').find('span').get('class')
            if arrow[0] == 'icon-Caret-up' and percent != '0.00%':
                plus = '+'
            elif arrow[0] == 'icon-Caret-down' and percent != '0.00%':
                plus = '-'
            else:
                plus = '='
        else:
            arrow = soup.find('span', class_='sc-15yy2pl-0 gEePkg').find('span').get('class')
            if arrow[0] == 'icon-Caret-up' and percent != '0.00%':
                plus = '+'
            elif arrow[0] == 'icon-Caret-down' and percent != '0.00%':
                plus = '-'
            else:
                plus = '='
        
        coins.append({
            'name': coin_name,
            'price': price,
            'link': link,
            'ticket': ticket,
            'percent': percent,
            'sign': plus
        })
    return coins


async def parse_every():
    while True:
        html = get_html(url)
        if html.status_code == 200:
            coins = []
            await asyncio.sleep(1)
            print("Parse")
            coins = get_content(get_url(html.text, url))
            for i in range(len(coins)):
                if not db.get_price(coins[i]['name']):
                    db.save_file(coins[i]['name'], coins[i]['price'], coins[i]['link'], coins[i]['ticket'], coins[i]['percent'], coins[i]['sign'])
                else:
                    db.update(coins[i]['price'], coins[i]['percent'], coins[i]['sign'], coins[i]['ticket'])
            print(coins)
        else:
            print("ERROR")
        await asyncio.sleep(120)
