from scrapy import cmdline
from datetime import date

today = date.today()
file = "scrapy crawl shopee-item -o data/shopee_"+str(today)+".csv"
# file = "scrapy crawl shopee-item -o data/tiki_"+str(today)+".csv"
# file = "scrapy crawl shopee-item -o data/sendo_"+str(today)+".csv"
# file = "scrapy crawl shopee-item -o data/lazada_"+str(today)+".csv"

cmdline.execute(file.split())
