from scrapy import cmdline
from datetime import date

today = date.today()
# file = "scrapy crawl shopee-item -o data/shopee/shopee_"+str(today)+".csv"
# file = "scrapy crawl tiki -o data/tiki/tiki_"+str(today)+".csv"
# file = "scrapy crawl sendo -o data/sendo/sendo_"+str(today)+".csv"
# file = "scrapy crawl lazada -o data/lazada/lazada_"+str(today)+".csv"

# file = "scrapy crawl shopee-item-all -o data/shopee/shopee_all_data.csv"
# file = "scrapy crawl tiki-all -o data/tiki/tiki_all_data.csv"
file = "scrapy crawl sendo-all -o data/sendo/sendo_all_data.csv"

# file = "scrapy crawl shopee-item -o data/shopee/shopee_data.csv"
# file = "scrapy crawl tiki -o data/tiki/tiki_data.csv"
# file = "scrapy crawl sendo -o data/sendo/sendo_data.csv"
# file = "scrapy crawl lazada -o data/lazada/lazada_data.csv"
cmdline.execute(file.split())
