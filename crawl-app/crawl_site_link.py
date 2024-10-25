from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode, parse_qs
import os

import validators
from bs4 import BeautifulSoup
import requests

from logging_config import logger

class CrawlSiteLink:
	def __init__(self) -> None:
		self.url = "https://trafficdata.tii.ie/tfmonthreport.asp?sgid=XzOA8m4lr27P0HaO3_srSB&spid=256365229484"
	
	def crawl(self):
		document = requests.get(self.url, timeout=30)
		html_doc = document.content
		soup = BeautifulSoup(html_doc, 'html.parser')
		site_eles = soup.select("ul.dropdown-menu li>a")
		res = []
		for ele in site_eles:
			href = ele['href']
			if validators.url(href):
				parsed_url = urlparse(href)
				query = dict(parse_qsl(parsed_url.query))
				query.pop('reportdate', None)
				query.pop('enddate', None)
				new_query = urlencode(query)
				new = parsed_url._replace(query=new_query)
				newUrl = urlunparse(new)
				res.append(newUrl)

		# ensure no duplicate link
		res = list(set(res))
		res.sort()
		part_nums = len(res) // 50 + 1 

		if not os.path.exists('./list-url'):
			os.makedirs("./list-url/")
			
		for part in range(part_nums):
			with open(f'./list-url/{part}.txt', 'w') as f:
				for i in res[part*50: (part+1)*50]:
					f.write(i)
					f.write('\n')

if __name__ == '__main__':
	crawl = CrawlSiteLink()
	crawl.crawl()