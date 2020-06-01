import scrapy
import json

## crawl lazada
class SendoSpider(scrapy.Spider):
    name = 'sendo'

    start_urls = [
        "https://www.sendo.vn/m/wap_v2/category/product?category_id=189&listing_algo=algo14&p=1&platform=web&s=60&sortType=listing_v2_location_desc"
    ]
    page_number = 2

    def parse(self, response):
        api_response = json.loads(response.text)
        list_items = api_response.get('result').get('data')

        for product in list_items:
            name = product['name']
            price = product['final_price']
            shop_name = product['shop_info']['shop_name']
            product_id = product['product_id']
            x = 0
            yield {
                'product_id': product_id,
                'name': name,
                'price': price,
                'shop_name': shop_name
            }

        next_page = 'https://www.sendo.vn/m/wap_v2/category/product?category_id=189&listing_algo=algo14&p=' + str(SendoSpider.page_number) + '&platform=web&s=60&sortType=listing_v2_location_desc/'
        if SendoSpider.page_number <= 60:
            SendoSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)