import scrapy
import json


## crawl lazada
class SendoSpider(scrapy.Spider):
    name = 'sendo'

    start_urls = [
        "https://www.sendo.vn/m/wap_v2/category/product?category_id=189&listing_algo=algo14&p=1&platform=web&s=60&sortType=listing_v2_location_desc"
    ]
    page_number = 2
    item_api = "https://mapi.sendo.vn/mob/product/{}/detail/"
    shop_api = "https://mapi.sendo.vn/mob/shop/{}/detail/"

    def parse_shop_api(self, response, product_name, final_price, product_id, product_url,shop_id):
        api_response = json.loads(response.text)
        shop_url = api_response['website']
        shop_name = api_response['shop_name']

        yield {
            'product_id': product_id,
            'product_url': product_url,
            'name': product_name,
            'price': final_price,
            'shop_id': shop_id,
            'shop_url': shop_url,
            'shop_name': shop_name,
        }

    def parse_item_api(self, response, product_id, product_name, final_price):
        api_response = json.loads(response.text)
        product_url = ""
        if "deep_link" in api_response:
            product_url = api_response['deep_link']
        admin_id = api_response['admin_id']
        shop_api_url = self.shop_api.format(admin_id)
        yield scrapy.Request(shop_api_url, callback=self.parse_shop_api,
                             cb_kwargs={'product_name': product_name,
                                        'final_price': final_price,
                                        'product_id': product_id,
                                        'product_url': product_url,
                                        'shop_id': admin_id})

    def parse(self, response):
        api_response = json.loads(response.text)
        list_items = api_response.get('result').get('data')

        for product in list_items:
            name = product['name']
            price = product['final_price']
            product_id = product['product_id']
            item_api_url = self.item_api.format(product_id)

            yield scrapy.Request(item_api_url, callback=self.parse_item_api,
                                 cb_kwargs={'product_id': product_id,
                                            'product_name': name,
                                            'final_price': price})


        next_page = 'https://www.sendo.vn/m/wap_v2/category/product?category_id=189&listing_algo=algo14&p=' + str(
            SendoSpider.page_number) + '&platform=web&s=60&sortType=listing_v2_location_desc/'
        if SendoSpider.page_number <= 60:
            SendoSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
