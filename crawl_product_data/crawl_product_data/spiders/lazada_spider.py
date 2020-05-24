import scrapy
import json

## crawl lazada
class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    start_urls = [
        # "https://www.lazada.vn/noi-tre-so-sinh/?ajax=true&spm=a2o4n.searchlistcategory.card.2.1fee29ebgMsiIB&item_id=309864813&from=onesearch_category_10657"
        # "https://www.lazada.vn/noi-tre-so-sinh/?ajax=true&page=1"
        # "https://www.lazada.vn/noi-tre-so-sinh/?ajax=true&from=onesearch_category_10657&item_id=309864813&page=2&spm=a2o4n.searchlistcategory.card.2.1fee29ebgMsiIB"
        "https://www.lazada.vn/noi-tre-so-sinh/?page=1&ajax=true"
    ]
    page_number = 2

    def parse(self, response):
        api_response = json.loads(response.text)
        list_items = api_response['mods']['listItems']

        for product in list_items:
            name = product['name']
            price = product['price']
            x = 0
            yield {
                'name': name,
                'price': price
            }

        next_page = 'https://www.lazada.vn/noi-tre-so-sinh/?ajax=true&page=' + str(LazadaSpider.page_number) + '/'
        if LazadaSpider.page_number <= 17:
            LazadaSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)