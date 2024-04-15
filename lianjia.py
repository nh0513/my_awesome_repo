import requests
from bs4 import BeautifulSoup
import mysql.connector

class LianJiaSpider():

    def __init__(self):
        self.url = 'https://bj.lianjia.com/chengjiao/pg{0}/'
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

    def send_request(self,url):
        resp = requests.get(url,headers=self.headers)
        if resp.status_code == 200:
            return resp

    def parse_html(self,resp):
        html = resp.text
        bs = BeautifulSoup(html,'lxml')
        ul = bs.find('ul',class_="listContent")
        li_list = ul.find_all('li')
        #print(len(li_list))
        for itme in li_list:
            title = itme.find('div',class_='title').text
            #positionInfo = itme.find('div',class_='positionInfo').text
            #houseInfo = itme.find('div',class_='houseInfo').text
            #totalPrice = itme.find('div',class_='totalPrice').text
            #unitPrice = itme.find('div',class_='unitPrice').text
            print(title)

    def save(self):
        pass

    def start(self):
        for i in range(1,2):
            full_url = self.url.format(i)
            resp = self.send_request(full_url)
            #print(resp.text)
            self.parse_html(resp)

if __name__ == '__main__':
    lianjia = LianJiaSpider()
    lianjia.start()
