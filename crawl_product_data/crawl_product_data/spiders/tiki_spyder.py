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
        'https://www.sendo.vn/giuong-cui-noi-cho-be/'
    ]
#?????
    page_number = 2

    def parse(self, response):
        # all_product_div = response.xpath('//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/div[@class="list_1VuX grid5_gtk-"]')
        all_product_div = response.css('div.caption_2Jn3')

        # product_title = //div[@class="ReactVirtualized__Grid__innerScrollContainer"]//div[@class="list_1VuX grid5_gtk-"]//span[@class="truncateMedium_Tofh"]
        # final_price = //div[@class="ReactVirtualized__Grid__innerScrollContainer"]//div[@class="list_1VuX grid5_gtk-"]//strong[@class="currentPrice_2hr9"]
        for product in all_product_div:
            product_title = product.xpath('.//span[@class="truncateMedium_Tofh"]').extract()[0]
            final_price = product.xpath('.//strong[@class="currentPrice_2hr9"]').extract()[0].strip()
            x = 0
            yield {
                'product_title': product_title,
                'final_price': final_price
            }
        #
        # next_page = 'https://www.sendo.vn/giuong-cui-noi-cho-be/?p=' + str(TikiSpider.page_number) + '/'
        # if TikiSpider.page_number <= 64:
        #     TikiSpider.page_number += 1
        #     yield response.follow(next_page, callable=self.parse())
