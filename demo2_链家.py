import requests
from bs4 import BeautifulSoup
import mysql.connector

class LianJiaSpider():
    mydh = mysql.connector.connect(host='localhost',user='root',password='nmf030226',database='week',auth_plugin ='mysql_native_password')
    mycursor = mydh.cursor()

    def __init__(self):
        self.url = 'https://bj.lianjia.com/ershoufang/pg{0}/'
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

    def send_request(self,url):
        resp = requests.get(url,headers=self.headers)
        if resp.status_code == 200:
            return resp

    def parse_html(self,resp):
        html = resp.text
        bs = BeautifulSoup(html,'lxml')
        ul = bs.find('ul',class_="sellListContent")
        li_list = ul.find_all('li')
        #print(len(li_list))
        self.lst = []
        for itme in li_list:

            title = itme.find('div',class_='title').text
            positionInfo = itme.find('div',class_='positionInfo').text
            houseInfo = itme.find('div',class_='houseInfo').text
            totalPrice = itme.find('div',class_='totalPrice').text
            unitPrice = itme.find('div',class_='unitPrice').text
            self.lst.append((title,positionInfo,houseInfo,totalPrice,unitPrice))
            #print(lst)
        self.save(self.lst)
    def save(self,lst):
        sql = 'insert into tb_lianjia(title,positionInfo,houseInfo,totalPrice,unitPrice) values (%s,%s,%s,%s,%s)'
        self.mycursor.executemany(sql,lst)
        self.mydh.commit()
        print(self.mycursor.rowcount,"插入完毕")

    def start(self):
        for i in range(1,2):
            full_url = self.url.format(i)
            resp = self.send_request(full_url)
            #print(resp.text)
            self.parse_html(resp)

if __name__ == '__main__':
    lianjia = LianJiaSpider()
    lianjia.start()