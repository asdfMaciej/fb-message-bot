import requests
from bs4 import BeautifulSoup
from random import randint


class Command:
	command_names = [
		'.modlitwa', '.deusvult', '.avemaria', '.maria',
		'.jezus', '.jesus', '.psalm', '.psalmy', '.biblia'
	]
	admin_only = False
	description = "Losowa modlitwa."

	@staticmethod
	def run(self, params_d):
		url = "http://www.biblia.deon.pl/otworz.php?skrot=Ps "
		cyferka = str(randint(1, 150))
		r = requests.get(url+cyferka)
		r.encoding = 'iso-8859-2'
		soup = BeautifulSoup(r.text)
		div = soup.find("div", {"class": "tresc"})
		params_d['functions_holder']._send_line(
			div.text, params_d['thread_id'], params_d['thread_type']
		)
