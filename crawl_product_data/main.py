from scrapy import cmdline
# cmdline.execute("scrapy crawl tiki -o data/tiki_product_data.csv".split())
# cmdline.execute("scrapy crawl lazada -o data/lazada_product_data.csv".split())
cmdline.execute("scrapy crawl sendo -o data/sendo_product_data.csv".split())
