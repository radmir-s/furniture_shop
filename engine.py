from bs4 import BeautifulSoup
import requests


def collect_item_urls(url):
    links = []
    with requests.get(url) as req:
        soup = BeautifulSoup(req.content, features='html.parser')
    items = soup.find_all(class_="wsite-com-category-product wsite-com-column ")
    for item in items:
        tail = item.find(class_="wsite-com-link wsite-com-category-product-link ")['href']
        TAIL = tail.upper()
        if 'NEW_ITEM_COMING_SOON' not in TAIL and 'OUT_OF_STOCK' not in TAIL and 'SOLD_OUT' not in TAIL:
            links.append('https://www.happyhomesindustries.com' + tail)
    return links


class Item:
    def __init__(self, url):
        self.url = url
        with requests.get(url) as req:
            soup = BeautifulSoup(req.content, features='html.parser')
        self.picture_link = 'https://www.happyhomesindustries.com' + soup.find('img', alt="Picture")['src']
        self.title = soup.find(id="wsite-com-product-title").text.strip()
        self.description = [par.text for par in soup.find_all("p") if par.text]

    @property
    def prices(self, cheap=100):
        prices = {}
        retail_on = False
        for string in self.description:
            if 'retail' in string.lower():
                retail_on = True
            if retail_on and string.strip().endswith('7'):
                l = string.split()
                price = float(l[-1].strip(" :")[1:-1])
                prices[l[0].strip(" :-")] = int(price * 1.8) if price > cheap else int(price * 1.6)
        return prices

    def save_image(self):
        req = requests.get(self.picture_link)
        with open(self.title + '.jpg', 'wb') as f:
            f.write(req.content)


def links_from_txt(file_name):
    with open(file_name, "r") as file:
        return file.read().split('\n')


def store_links(links):
    with open("item_links.txt", mode='w') as file:
        for link in links:
            file.write(link + '\n')
