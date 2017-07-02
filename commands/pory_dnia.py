import requests
import json
from dateutil import tz
from datetime import datetime


class Command:
	command_names = [
		'.dzien', '.dzień', '.pory', '.fazy', '.goldenhour',
		'.wschód', '.wschod', '.zachod', '.zachód'
	]
	admin_only = False
	description = "Pokazuje pory obecnego dnia."

	@staticmethod
	def run(self, params_d):
		def tt(old):
			from_zone = tz.tzutc()
			retarded = datetime.now().strftime('%Y%m%d')
			time_tuple = datetime.strptime(old+retarded, "%I:%M:%S %p%Y%m%d").replace(tzinfo=from_zone)
			time_tuple = time_tuple.astimezone(tz=None)
			return time_tuple.strftime("%H:%M:%S")

		url_api = 'https://api.sunrise-sunset.org/json?lat=52.7145775&lng=16.3705298&date=today'
		r = requests.get(url_api).text
		jsn = json.loads(r)
		if jsn['status'] == 'OK':
			dlugosc_dnia = jsn['results']['day_length']
			cool_text = "Długość dzisiejszego dnia wynosi: "+dlugosc_dnia+".\n"
			cool_text += "Świt astronomiczny: " + tt(jsn['results']['astronomical_twilight_begin'])+".\n"
			cool_text += "Świt żeglarski: " + tt(jsn['results']['nautical_twilight_begin'])+".\n"
			cool_text += "Świt cywilny: " + tt(jsn['results']['civil_twilight_begin'])+".\n"
			cool_text += "Wschód: " + tt(jsn['results']['sunrise'])+".\n"
			cool_text += "Południe astronomiczne: " + tt(jsn['results']['solar_noon'])+".\n"
			cool_text += "Zachód: " + tt(jsn['results']['sunset'])+".\n"
			cool_text += "Zmierzch cywilny: " + tt(jsn['results']['civil_twilight_end'])+".\n"
			cool_text += "Zmierzch żeglarski: " + tt(jsn['results']['nautical_twilight_end'])+".\n"
			cool_text += "Zmierzch astronomiczny: " + tt(jsn['results']['astronomical_twilight_end'])+"."
		else:
			cool_text = "api.sunrise-sunset.org zwróciło zły status - "+jsn['status']
		params_d['functions_holder']._send_line(
			cool_text, params_d['thread_id'], params_d['thread_type']
		)
