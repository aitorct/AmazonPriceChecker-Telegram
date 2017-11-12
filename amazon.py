import requests
from lxml import html
import re
import string


def checkPrice(url):
    response = requests.get(url)
    while(response.status_code != 200):
        response = requests.get(url)
    website = html.fromstring(response.content)
    price = None
    
    try:
        price = website.xpath("//span[@id='priceblock_saleprice']/text()")[0]
    except IndexError:
        pass

    try:
        price = website.xpath("//span[@id='priceblock_ourprice']/text()")[0]
    except IndexError:
        pass

    return re.sub("[^0123456789\.,]", "", price)


def getName(url):
    response = requests.get(url)
    while(response.status_code != 200):
        response = requests.get(url)
    website = html.fromstring(response.content)

    return website.xpath("//span[@id='productTitle']/text()")[0]
