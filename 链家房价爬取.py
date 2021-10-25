import requests
from lxml import etree
import csv
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

fp = open('D://链家房价.csv','wt',newline='',encoding='utf8')
writer = csv.writer(fp)
writer.writerow(('楼盘', '地址', '房间', '面积', '价格', '起价', '优点'))

def makesoup(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf8')

def get_info(html):
    selector = etree.HTML(html)
    li_list = selector.xpath(
        '//li[contains(@class, "resblock-list")]/div[@class="resblock-desc-wrapper"]')
    for k in li_list:
        name = k.xpath(
            "div[@class='resblock-name']/a[@class='name ']/text()")[0]
        adress_1 = k.xpath(
            "div[@class='resblock-location']/span[1]/text()")[0]
        adress_2 = k.xpath(
            "div[@class='resblock-location']/span[2]/text()")[0]
        adress_3 = k.xpath("div[@class='resblock-location']/a/text()")[0]
        adress = adress_1 + '/' + adress_2 + '/' + adress_3
        home_num_1 = k.xpath("a[@class='resblock-room']/span[1]/text()")
        home_num_2 = k.xpath("a[@class='resblock-room']/span[2]/text()")
        home_num_3 = k.xpath("a[@class='resblock-room']/span[3]/text()")
        if home_num_1:
            home_num_1 = home_num_1[0]
            if home_num_2:
                home_num_1 = home_num_1 + '/' + home_num_2[0]
                if home_num_3:
                    home_num_1 = home_num_1 + '/' + home_num_3[0]
                else:
                    pass
            else:
                pass   
        else:
            home_num_1 = ''
        area = k.xpath("div[@class='resblock-area']/span/text()")
        if area :
            area = area[0]
        price = k.xpath("div[@class='resblock-price']/div[@class='main-price']/span[@class='number']/text()")[0]
        price += '元/平(均价)'
        minimum_price = k.xpath("div[@class='resblock-price']/div[@class='second']/text()")
        if minimum_price:
            minimum_price = minimum_price[0]
        advantge = k.xpath("div[@class='resblock-tag']//text()")
        mylist = []
        for K in advantge:
            j = K.strip()
            if j :
                mylist.append(j)
            else:
                pass
        advantge = '，'.join(mylist)
        x = [name, adress, home_num_1, area, price,  minimum_price, advantge]
        print(x)
        writer.writerow(x)

if __name__ == '__main__':
    urls = ['https://dl.fang.lianjia.com/loupan/pg{}/'.format(i) for i in range(1,39)]
    for url in urls:       
        html = makesoup(url)
        get_info(html)
        time.sleep(3)
