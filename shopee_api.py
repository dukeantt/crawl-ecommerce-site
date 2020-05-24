from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


class HtmlGetter:
    def get_html(self, url):
        pass


class HtmlParseGetter(HtmlGetter):
    def __init__(self, subject):
        self.subject = subject

    def get_html(self, url):
        html_source = self.subject.get_html(url)
        html_element = html.fromstring(html_source)
        return html_element


class SeleniumHtmlGetter(HtmlGetter):
    def __init__(self, scroll_to_bottom=True):
        self.scroll_to_bottom = scroll_to_bottom

    def get_html(self, url):
        # browser = webdriver.PhantomJS("C:/Users/ngduc/Downloads/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        browser = webdriver.Chrome("C:/Users/ngduc/Downloads/chromedriver_win32/chromedriver.exe")

        browser.get(url)
        if self.scroll_to_bottom:
            last = None
            time.sleep(2)
            for v in range(500):
                for k in range(5):
                    browser.find_element_by_xpath('//html').send_keys(Keys.DOWN)
                if last is not None and last == browser.execute_script('return window.pageYOffset;'):
                    print(url)
                    break
                last = browser.execute_script('return window.pageYOffset;')
        html_source = browser.page_source
        browser.quit()
        return html_source


if __name__ == '__main__':
    url = 'https://shopee.vn/Xe-%C4%91%E1%BA%A9y-n%C3%B4i-c%C5%A9i-cat.163.2350.8851?page=0'
    html_getter = HtmlParseGetter(SeleniumHtmlGetter())
    name = []
    price = []
    # page_list = [2, 4, 6, 10, 15, 17, 18, 19, 21, 25, 26, 28, 30, 35, 36, 39, 44, 48, 50, 51, 61, 62, 70, 73, 75, 76, 77, 80, 81, 82, 84, 86, 87, 88, 89, 94, 96, 97]
    # page_list = [6, 10, 15, 19, 25, 26, 28, 35, 36, 62, 75, 76, 77, 81, 88, 89, 94, 96]
    # page_list = [15,19,25,26, 77,94, 96]
    page_list = [97,98,99]

    for i in range(1, 100):
    # for i in page_list:
        html_tree = html_getter.get_html(url)

        for v in html_tree.xpath("//div[@class='_3eufr2']"):
            product_name = v.xpath(".//div[@class='_1NoI8_ _16BAGk']/text()")
            if len(product_name) <= 0:
                product_name = v.xpath(".//div[@class='_1NoI8_ _1JBBaM']/text()")
            product_price = v.xpath(".//div[@class='_1w9jLI _37ge-4 _2ZYSiu']/span[@class='_341bF0']/text()")
            if len(product_name) > 0 and len(product_price) > 0:
                name.append(str(product_name[0]))
                price.append(str(product_price[0]).replace(".", ""))
                print(str(product_name[0])+" - "+str(product_price[0]).replace(".", ""))
                # print(str(product_price[0]).replace(".", ""))
                # print()
            else:
                x = 0
                print(product_name)
                print(product_price)
        # url = 'https://shopee.vn/search?keyword=xe%20%C4%91%E1%BA%A9y,%20n%C3%B4i%20c%C5%A9i&page=' + str(i)
        url = 'https://shopee.vn/Xe-%C4%91%E1%BA%A9y-n%C3%B4i-c%C5%A9i-cat.163.2350.8851?page=' + str(i)
    dict = {'name': name, 'price': price}
    df = pd.DataFrame(dict,columns=['name','price'])
    df.to_csv(r'shopee_product_data_20_5_2020_1.csv', index=False, header=True)


'''
page 1
2 4 6 10 15 17 18 19 21 25 26 28 30 35 36 39 44 48 50 51 61 62 70 73 75 76 77 80 81 82 84 86 87 88 89 94 96 97 
6 10 15 19 25 26 28 35 36 62 75 76 77 81 88 89 94 96
'''