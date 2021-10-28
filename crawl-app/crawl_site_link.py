from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode, parse_qs


import validators
from bs4 import BeautifulSoup
import requests

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
		with open('./list-url.txt', 'w') as f:
			for i in res:
				f.write(i)
				f.write('\n')

if __name__ == '__main__':
	crawl = CrawlSiteLink()
	crawl.crawl()