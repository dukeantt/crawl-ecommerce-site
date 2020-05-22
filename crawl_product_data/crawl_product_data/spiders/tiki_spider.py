import scrapy


## crawl tiki
class TikiSpider(scrapy.Spider):
    name = 'tiki'
    '''
    tiki: https://tiki.vn/noi/c10468
    sendo: https://www.sendo.vn/giuong-cui-noi-cho-be/
    shopee: https://shopee.vn/Xe-%C4%91%E1%BA%A9y-n%C3%B4i-c%C5%A9i-cat.163.2350.8851
    lazada: https://www.lazada.vn/noi-tre-so-sinh/?spm=a2o4n.searchlistcategory.card.2.1fee29ebgMsiIB&item_id=309864813&from=onesearch_category_10657
    lazada: https://www.lazada.vn/giuong-noi/?spm=a2o4n.searchlistcategory.card.6.1fee29ebRUgYLd&item_id=399328790&from=onesearch_category_10657
    '''
    start_urls = [
        'https://tiki.vn/noi/c10468?page=1'
    ]
    page_number = 2

    def parse(self, response):
        all_product_div = response.xpath('//div[contains(@class, \'product-box-list\')]/div')
        # product_title = response.xpath('//div[contains(@class, \'product-box-list\')]/div/@data-title').extract()
        # title = response.xpath('string(//div[contains(@class, \'product-box-list\')]/div/@data-title)').extract()
        # final_price = response.css('.final-price::text').extract()
        # final_price[0].strip()
        # //div[contains(@class, 'product-box-list')]/div//span[@class='final-price']
        for product in all_product_div:
            product_title = product.xpath('@data-title').extract()[0]
            final_price = product.xpath('.//span[@class=\'final-price\']/text()').extract()[0].strip()
            x = 0
            yield {
                'name': product_title,
                'price': final_price
            }

        next_page = 'https://tiki.vn/noi/c10468?page=' + str(TikiSpider.page_number)
        if TikiSpider.page_number <= 4:
            TikiSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
