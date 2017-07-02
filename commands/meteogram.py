from run_bot import CustomClient, QueueEvent
import requests


class Command:
	command_names = [
		'.pogoda', '.meteogram'
	]
	admin_only = False
	description = "Pokazuje meteogram z Wronek (meteo.pl)."

	@staticmethod
	def run(self, params_d):
		url_pl = 'http://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate={}&row=391&col=171&lang=pl'
		url_meteogram = 'http://new.meteo.pl/um/php/meteorogram_id_um.php?ntype=0u&id=2658'
		r = requests.get(url_meteogram)
		data = r.text.split('var fcstdate = "')[1].split('";')[0]
		url_pl = url_pl.format(data)
		txt = 'Meteogram dla stacji Wronki (meteo.pl): '
		img = requests.get(url_pl)
		with open('temp/obrazek.png', 'wb+') as f:
			if r.status_code == 200:
				for chunk in img:
					f.write(chunk)

		params_d['callback'].queue.append(
			QueueEvent(
				params_d['callback'], CustomClient.send_image_local, 'temp/obrazek.png', 
				txt, params_d['thread_id'], params_d['thread_type']
			)
		)
