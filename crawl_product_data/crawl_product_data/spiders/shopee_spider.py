import scrapy
import json

## crawl shopee
class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    start_urls = [
        "https://shopee.vn/api/v2/search_items/?by=relevancy&keyword=Xe%20%C4%91%E1%BA%A9y%2C%20n%C3%B4i%20c%C5%A9i&limit=50&match_id=8851&newest=0&order=desc&page_type=search&version=2"
    ]
    newest = 50

    def parse(self, response):
        api_response = json.loads(response.text)
        list_items = api_response['items']

        for product in list_items:
            name = product['name']
            price = product['price']
            x = 0
            yield {
                'name': name,
                'price': price
            }

        next_page = 'https://shopee.vn/api/v2/search_items/?by=relevancy&keyword=Xe%20%C4%91%E1%BA%A9y%2C%20n%C3%B4i' \
                    '%20c%C5%A9i&limit=50&match_id=8851&newest=' + str(ShopeeSpider.newest) + '&order=desc&page_type=search&version=2'
        if ShopeeSpider.newest <= 5000:
            ShopeeSpider.newest += 50
            yield response.follow(next_page, callback=self.parse)