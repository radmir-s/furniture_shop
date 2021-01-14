from bs4 import BeautifulSoup
import requests
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
from os import remove


def collect_item_urls(url):
    links = []
    with requests.get(url) as req:
        soup = BeautifulSoup(req.content, features='html.parser')
    items = soup.find_all(class_="wsite-com-category-product wsite-com-column ")
    for item in items:
        tail = item.find(class_="wsite-com-link wsite-com-category-product-link ")['href']
        TAIL = tail.upper()
        if 'NEW_ITEM_COMING_SOON' not in TAIL:
            links.append('https://www.happyhomesindustries.com' + tail)
    return links


class Item:
    def __init__(self, url):
        self.url = url
        with requests.get(url) as req:
            soup = BeautifulSoup(req.content, features='html.parser')
        self.picture_link = 'https://www.happyhomesindustries.com' + soup.find('a', class_="cloud-zoom")['href']
        self.title = soup.find(id="wsite-com-product-title").text.strip()
        self.description = [par.text for par in soup.find_all("p") if par.text]
        self.sold_out = soup.find(id="wsite-com-product-inventory-out-of-stock-message").text.strip()

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
        image_name = self.title + '.jpg'
        if '/' in image_name:
            image_name = image_name.split('/')[-1]
        with open(image_name, 'wb') as f:
            f.write(req.content)
        return image_name


def data_from_txt(file_name):
    with open(file_name, "r") as file:
        return file.read().split('\n')


def store_items_data(items):
    zip_file_name = "furniture " + datetime.now().strftime("%m-%d-%Y %H-%M-%S") + ".zip"
    csv_name = zip_file_name[:-4] + ".csv"
    zip_file = ZipFile(zip_file_name, "w")
    with open(csv_name, mode='w') as file:
        file.write('#, Title, Sold_out?, Description, Link \n')
        count = 1
        for item in items:
            file.write(f"{count}, {item.title}, {item.sold_out}, {item.description}, {item.url}\n")
            image_name = item.save_image()
            zip_file.write(image_name, compress_type=ZIP_DEFLATED)
            remove(image_name)
            count += 1
    zip_file.write(csv_name, compress_type=ZIP_DEFLATED)
    remove(csv_name)
    return zip_file_name


def get_item_links():
    item_links = []
    for url in links_from_txt('section_links.txt'):
        item_links.extend(collect_item_urls(url))
    return item_links


def links_from_txt(file_name):
    with open(file_name, "r") as file:
        return file.read().split('\n')


def get_items(item_links):
    items = []
    for link in item_links:
        items.append(Item(link))
    return items


if __name__ == "__main__":
    item_links = get_item_links()
    items = get_items(item_links)
    store_items_data(items)
