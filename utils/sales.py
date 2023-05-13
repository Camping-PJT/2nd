import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.ocamall.com/shop/shopbrand.html?xcode=072&type=Y'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.39.132 Safari/53.36'}
response = requests.get(url, verify=False, headers=headers, timeout=30)

# Try different encodings until the text is correctly decoded
encodings = ['utf-8', 'euc-kr', 'cp949']
text = None
for encoding in encodings:
    try:
        text = response.content.decode(encoding)
        break
    except UnicodeDecodeError:
        continue

soup = BeautifulSoup(text, 'html.parser')
items = soup.select('div.goodsListWrap.grid4 > ul > li')


def item():
    rank = 1
    item_list = {}
    for item in items:
        link = 'https://www.ocamall.com'+item.select_one('a')['href']
        img_url = 'https://www.ocamall.com/'+item.select_one('a > div.imgWrap > img')['src']
        company = item.select_one('p.companyName').text
        goods = re.sub(r'\[[^\]]*\]', '',item.select_one('p.goodsName').text)
        customerPrice = item.select_one('strong.customerPrice').text
        sellPrice = item.select_one('strong.sellPrice').text

        if customerPrice and sellPrice:
          cp, sp = int(customerPrice.replace(",", "")), int(sellPrice.replace(",", ""))
          if cp-sp == 0:
            discount = ''
          else:
            discount = str(int(round((cp-sp)/cp*100,0)))+'%'
        else:
            discount = ''
        item_list[rank] = [img_url, company, goods, discount, customerPrice, sellPrice, link]
        rank += 1
        if rank == 25:
            break
    return item_list
