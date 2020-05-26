# -*- coding: utf-8 -*-
import logging
import scrapy
import json


class ShopeeItemSpider(scrapy.Spider):
    name = 'shopee-item-all'
    allowed_domains = ['shopee.vn']

    # cat_api = 'https://shopee.vn/api/v2/search_items/?by=relevancy&keyword={}' \
    #           '%C5%A9i&limit=50&match_id=8851&newest={}&order=desc&page_type=search&version=2 '
    cat_api = "https://shopee.vn/api/v2/search_items/?by=relevancy&limit=50&match_id=163&newest={}&order=desc" \
              "&page_type=search&version=2 "
    item_api = "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}"
    item_url = "https://shopee.vn/product/{}/{}"

    search_text = "Xe đẩy, nôi cũi"
    item_limit = 50
    cat_id = 1979
    start_id = 0

    max_retry_empty_list = 3

    item_topic = 'shopee_items_raw'
    review_topic = 'shopee_reviews_raw'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(item_topic=crawler.settings.get('SHOPEE_ITEMS_TOPIC'),
                   review_topic=crawler.settings.get('SHOPEE_REVIEWS_TOPIC'),
                   crawler=crawler, *args, **kwargs)

    def __init__(self, item_topic, review_topic, *args, **kwargs):
        self.item_topic = item_topic
        self.review_topic = review_topic
        super(ShopeeItemSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = self.cat_api.format(self.search_text, self.start_id)
        yield scrapy.Request(url, callback=self.parse_item_list,
                             cb_kwargs={'first_id': self.start_id, 'retry': 0})

    def parse_item_list(self, response, first_id, retry):
        jsonresponse = json.loads(response.text)

        item_list = jsonresponse.get('items', [])
        # for item in item_list:
        if item_list:
            for idx, item in enumerate(item_list):
                itemid, shopid = item['itemid'], item['shopid']
                api_url = self.item_api.format(itemid, shopid)
                yield scrapy.Request(api_url, callback=self.parse_item_api,
                                     cb_kwargs={'itemid': itemid,
                                                'shopid': shopid})

        if first_id < 5000:
            offset = first_id + self.item_limit
            url = self.cat_api.format(self.search_text, offset)
            if not item_list:
                retry += 1
            yield scrapy.Request(url, callback=self.parse_item_list,
                                 cb_kwargs={'first_id': offset, 'retry': retry})

    def parse_item_api(self, response, itemid, shopid):
        api_response = json.loads(response.text)
        if not 'item' in api_response \
                or not api_response['item'] \
                or not api_response['item']['price']:
            logging.warning("Potentially banned!!! Response: %s", response.text)
        url = self.item_url.format(shopid, itemid)
        item = api_response['item']
        name = item['name']
        name = name.replace("\"", "")
        price = str(item['price'] / 100000)
        yield {
            'name': name,
            'price': price
        }
