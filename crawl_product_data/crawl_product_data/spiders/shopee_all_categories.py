# -*- coding: utf-8 -*-
import logging
import scrapy
import json
from datetime import date


class ShopeeItemSpider(scrapy.Spider):
    name = 'shopee-item-all'
    allowed_domains = ['shopee.vn']
    # category : Mẹ và bé
    cat_api = 'https://shopee.vn/api/v2/search_items/?by=relevancy&limit=50&match_id=163&newest={}&order=desc' \
              '&page_type=search&version=2 '
    item_api = "https://shopee.vn/api/v2/item/get?itemid={}&shopid={}"
    shop_api = "https://shopee.vn/api/v2/shop/get?shopid={}"
    item_url = "https://shopee.vn/product/{}/{}"

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
        url = self.cat_api.format(self.start_id)
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

        if first_id < 20000:
            offset = first_id + self.item_limit
            url = self.cat_api.format(offset)
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
        name = name.replace("🌟", "")
        name = name.replace("\"", "")
        price = str(item['price'] / 100000)
        item_id = itemid
        shop_api_url = self.shop_api.format(shopid)
        today = date.today()

        # yield {
        #     'product_id': item_id,
        #     'product_url': url,
        #     'name': name,
        #     'price': price,
        #     'shop_id': shopid,
        #     'date': today,
        #     # 'shop_url': shop_url,
        #     # 'shop_name': shop_name,
        #     # 'shop_owner': shop_owner
        # }
        yield scrapy.Request(shop_api_url, callback=self.parse_shop_api,
                             cb_kwargs={'prod_name': name,
                                        'price': price,
                                        'item_id': item_id,
                                        'product_url': url})

    def parse_shop_api(self, response, prod_name, price, item_id, product_url):
        api_response = json.loads(response.text)
        shop_data = api_response['data']
        shop_id = shop_data['shopid']
        shop_url = ""
        shop_owner = ""
        shop_name = ""

        if "username" in shop_data['account']:
            shop_owner = shop_data['account']['username']
            shop_url = "https://shopee.vn/" + shop_owner
        if "name" in shop_data:
            shop_name = shop_data['name']
        today = date.today()

        yield {
            'product_id': item_id,
            'product_url': product_url,
            'name': prod_name,
            'price': price,
            'shop_id': shop_id,
            'shop_url': shop_url,
            'shop_name': shop_name,
            'shop_owner': shop_owner,
            'date': today,
        }
