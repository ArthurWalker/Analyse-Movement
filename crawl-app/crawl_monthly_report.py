from typing import List
import pandas as pd
from pandas.core import base 
import requests 
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, parse_qsl, urlencode, urlunparse
import os 
import datetime
from requests.models import PreparedRequest
import time
from dateutil.relativedelta import relativedelta


class Crawler:
	def __init__(self, base_report_url: str) -> None:
		self.SAVE_FOLDER = os.path.join(os.getcwd(), "craw_data")
		self.base_report_url = base_report_url

	def _get_siteId(self, soup: BeautifulSoup) -> str:
		siteId_ele = soup.select('div#content #subtitlebar span')[1]
		siteId_text = siteId_ele.text.split(":")[1].strip()
		siteId_text = str(int(siteId_text))
		return siteId_text
	
	def _get_monthly_data(self, soup: BeautifulSoup) -> pd.DataFrame:
		list_tr_element = soup.select("table#gridTable tr")
		content = []
		for i in range(1, len(list_tr_element)):
			tr_element = list_tr_element[i]
			if i == 1:
				# header 
				ths = tr_element.select('th')
				for j in range(len(ths)):
					content.append([ths[j].text])
			else:
				tds = tr_element.select('td')
				for j in range(len(tds)):
					content[j].append(tds[j].text)

		# convert content to pandas dataframe
		df = pd.DataFrame(content)
		df = df.transpose()
		new_header = df.iloc[0]
		df = df[1:]
		df.columns = new_header

		df.index = df['Time']
		df = df.drop(columns=['Time'], axis=1)
		return df
	
	
	def get_montly_report_by_url(self, url: str) -> None:
		parsed_url = urlparse(url)
		query = parse_qs(parsed_url.query)
		report_date = query['reportdate'][0]
		document = requests.get(url, timeout=30)
		html_doc = document.content
		soup = BeautifulSoup(html_doc, 'html.parser')
		siteId_text = self._get_siteId(soup)
		df = self._get_monthly_data(soup)
		# save it to csv file 
		outfile_folfer = os.path.join(self.SAVE_FOLDER, report_date)
		if not os.path.exists(outfile_folfer):
			os.makedirs(outfile_folfer)
		print(f'output folder: {outfile_folfer}')
		df.to_csv(os.path.join(outfile_folfer, siteId_text + ".csv"))

	def _generate_date_inclusive(self, start_date: str, end_date:str) -> List[str]:
		res = []
		DATETIME_FORMAT = "%Y-%m-%d"
		start = datetime.datetime.strptime(start_date, DATETIME_FORMAT)
		end = datetime.datetime.strptime(end_date, DATETIME_FORMAT)
		i = start
		while i <= end:
			res.append(i.strftime(DATETIME_FORMAT))
			i = i + relativedelta(months=1)
		return res 

	def get_monthly_report(self, start_date: str, end_date: str) -> None:
		url = self.base_report_url
		date_range_list = self._generate_date_inclusive(start_date, end_date)
		count = 0
		for date in date_range_list:
			count += 1
			if count % 20 == 0:
				print("sleep: ", count)
				time.sleep(10)
			params = {'reportdate': date}
			new_url = self._add_params_url(url, params)
			print('\n\nstart processing for date: ', date, 'url: ', new_url)
			self.get_montly_report_by_url(url=new_url)
			print('Done for date: ', date)
		# note already crawl link 
		with open('./already_crawl_month_data.txt', 'a') as f:
			f.write(url)
			f.write('\n')
	
	def _add_params_url(self, url: str, params: dict) -> str:
		parsed_url = urlparse(url)
		query = dict(parse_qsl(parsed_url.query))
		query.update(params)
		new_query = urlencode(query)
		new = parsed_url._replace(query=new_query)
		newUrl = urlunparse(new)
		return newUrl


if __name__ == '__main__':
	base_url = "https://trafficdata.tii.ie/tfmonthreport.asp?sgid=XzOA8m4lr27P0HaO3_srSB&spid=55f9e7ad6213"
	crawl = Crawler(base_report_url=base_url)
	# start = datetime.datetime.now()
	# res = crawl.get_monthly_report('2020-02-01', '2021-09-01')
	# period = datetime.datetime.now() - start
	# print("total time: ", period)
	# print(crawl._generate_date_inclusive('2020-02-01', '2021-09-01'))

	params = {'reportdate': '2020-02-01'}
	new_url = crawl._add_params_url(base_url, params)
	print(new_url)
