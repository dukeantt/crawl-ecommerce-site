import logging
import scrapy
import json


## crawl tiki
class TikiSpider(scrapy.Spider):
    name = 'tiki'
    start_urls = [
        'https://tiki.vn/noi/c10468?page=1'
    ]
    page_number = 2
    item_api = "https://tiki.vn/api/v2/products/{}"

    def parse_item_api(self, response, product_name, final_price):
        api_response = json.loads(response.text)
        current_seller = api_response['current_seller']
        shop_name = current_seller['name']
        shop_id = current_seller['id']
        product_id = api_response['id']
        product_id2 = current_seller['product_id']
        shop_url = current_seller['link']
        product_url = "https://tiki.vn/" + api_response['url_path']

        yield {
            "product_id": product_id,
            "product_url": product_url,
            'name': product_name,
            'price': final_price,
            "shop_id": shop_id,
            "shop_url": shop_url,
            "shop_name": shop_name,
            "product_id2": product_id2
        }

    def parse(self, response):
        all_product_div = response.xpath('//div[contains(@class, \'product-box-list\')]/div')
        for product in all_product_div:
            product_title = product.xpath('@data-title').extract()[0]
            product_id = product.xpath('@data-id').extract()[0]
            final_price = product.xpath('.//span[@class=\'final-price\']/text()').extract()[0].strip()

            item_api_url = self.item_api.format(product_id)

            yield scrapy.Request(item_api_url, callback=self.parse_item_api,
                                 cb_kwargs={'product_name': product_title,
                                            'final_price': final_price})

        next_page = 'https://tiki.vn/noi/c10468?page=' + str(TikiSpider.page_number)
        if TikiSpider.page_number <= 4:
            TikiSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
