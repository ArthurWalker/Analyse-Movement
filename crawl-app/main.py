from crawl_monthly_report import Crawler
from logging_config import logger 
from helper import Helper


class MainApp:
	def __init__(self) -> None:
		self.already_crawl_file = './already_crawl_month_data.txt'
		self.crawl_site_file = './list-url/7.txt'
		self.START_DATE = '2020-02-01'
		self.END_DATE = '2021-09-01'

		Helper.init()
	
	def run(self):
		# load data from already_crawl file. 
		already_crawl_set = set()
		with open(self.already_crawl_file, 'r') as r:
			for line in r:
				already_crawl_set.add(line.strip())
		

		list_crawl_site = []
		with open(self.crawl_site_file, 'r') as r:
			for tmp in r:
				tmp = tmp.strip()
				if tmp not in already_crawl_set:
					list_crawl_site.append(tmp)
				
		
		# actual craw. can do multiple thread here 
		# list_crawl_site = list_crawl_site[:1] # for testing
		logger.info(f'number link need to be crawl: {len(list_crawl_site)}' )
		for crawl_site in list_crawl_site:
			crawler = Crawler(crawl_site)
			crawler.get_monthly_report(self.START_DATE, self.END_DATE)

if __name__ == '__main__':
	app = MainApp()
	logger.info('app running')
	app.run()
	