import os 
import random 
import config 
import requests
from logging_config import logger

class Helper:
	
	user_agents = []

	@staticmethod
	def init():
		with open(config.USER_AGENT_FILE_PATH, 'r') as r:
			for line in r:
				Helper.user_agents.append(line.strip())


	@staticmethod
	def random_user_agent():
		index =  random.randint(0, len(Helper.user_agents)-1)
		user_agent = Helper.user_agents[index]
		return user_agent
	
	@staticmethod
	def request_get(url: str) -> requests.models.Response:
		user_agent = Helper.random_user_agent()
		headers = {
    		'User-Agent': user_agent,
		}
		try:
			response =  requests.get(url, headers=headers, timeout=30)
		except Exception as e:
			logger.exception(e)
		return response
		
	


if __name__ == '__main__':
	Helper.init()
	url = 'https://trafficdata.tii.ie/tfdayreport.asp?sgid=XzOA8m4lr27P0HaO3_srSB&spid=4E30484E302E&reportdate=2020-12-30&enddate=2020-12-30&intval=2'
	Helper.request_get(url)
	Helper.request_get(url)