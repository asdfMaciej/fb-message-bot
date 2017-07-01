from fbchat import Client
from fbchat.models import *
from datetime import datetime
from dateutil import tz
import time
import enum
import sys
import threading
import multiprocessing
import requests
import re
import json
import calendar
import time
import sqlite3
import configparser

class DatabaseHandler:
	def __init__(self, db_name, callback):
		self.db_name = db_name
		self.con = -1
		self.callback = callback
		self.killed = False
		self.need_commit = False

	def tt(self, thr):
		if thr == ThreadType.GROUP:
			return "GROUP"
		else:
			return "USER"

	def __first_launch__(self):
		create_query = """
		CREATE TABLE uzytkownicy(fb_id TEXT, nazwa TEXT, pseudonim TEXT)
		CREATE TABLE grupy(fb_id TEXT, nazwa TEXT, uzytkownicy_id TEXT)
		CREATE TABLE wiadomosci(ts INT, nadawca TEXT, adresat TEXT, tekst TEXT, src TEXT, thread_type TEXT)
		CREATE TABLE obrazki(ts INT, nadawca TEXT, adresat TEXT, url TEXT, height INT, width INT, src TEXT, thread_type TEXT)
		CREATE TABLE naklejki(ts INT, nadawca TEXT, adresat TEXT, sticker_id TEXT, url TEXT, src TEXT, thread_type TEXT)
		CREATE TABLE filmy(ts INT, nadawca TEXT, adresat TEXT, url TEXT, height INT, width INT, length INT, type INT, rotation INT, src TEXT, thread_type TEXT)
		"""
		for row in create_query.strip().split('\n'):
			a = row.strip()
			if a: self.con.execute(a)

	def run(self):
		self.con = sqlite3.connect(self.db_name, check_same_thread=False)
		_c = self.con.cursor()
		_c.execute("SELECT fb_id from uzytkownicy")
		self.uzytkownicy_id = list(sum(_c.fetchall(), ()))  # flattens the list
		_c.execute("SELECT fb_id, uzytkownicy_id from grupy")
		self.grupy_id = {key: value for (key, value) in _c.fetchall()}
		while True:
			if self.killed:
				self.con.commit()
				self.con.close()
				break
			if self.need_commit:
				self.con.commit()
				if self.callback.debug:
					print('Commited database!')
				self.need_commit = False
			time.sleep(self.callback.db_save_delay)

	def add_uzytkownik(self, fb_id, nazwa, pseudonim):
		cursor = self.con.cursor()
		cursor.execute("SELECT * from uzytkownicy WHERE fb_id = (?)", (fb_id,))
		matches = cursor.fetchall()
		if matches:
			cursor.execute("UPDATE uzytkownicy SET nazwa = (?), pseudonim = (?) WHERE fb_id = (?)", (nazwa, pseudonim, fb_id))
			if self.callback.debug: print('Already was - updating')
		else:
			cursor.execute("INSERT INTO uzytkownicy VALUES (?,?,?)", (fb_id, nazwa, pseudonim))
			self.uzytkownicy_id.append(fb_id)
			if self.callback.debug: print('Wasnt - adding')
		self.need_commit = True

	def add_grupa(self, fb_id, nazwa, uzytkownicy):
		uzytkownicy += ','+self.callback.id
		cursor = self.con.cursor()
		cursor.execute("SELECT * from grupy WHERE fb_id = (?)", (fb_id,))
		matches = cursor.fetchall()
		if matches:
			cursor.execute("UPDATE grupy SET nazwa = (?), uzytkownicy_id = (?) WHERE fb_id = (?)", (nazwa, uzytkownicy, fb_id))
			if self.callback.debug: print('Already was - updating [gr]')
		else:
			cursor.execute("INSERT INTO grupy VALUES (?,?,?)", (fb_id, nazwa, uzytkownicy))
			if self.callback.debug: print('Wasnt - adding [gr]')
		self.grupy_id[fb_id] = uzytkownicy
		self.need_commit = True

	def add_wiadomosc(self, ts, nadawca, adresat, tekst, src, thread_type):
		cursor = self.con.cursor()
		cursor.execute(
			"INSERT INTO wiadomosci VALUES (?,?,?,?,?,?)", 
			(ts, nadawca, adresat, tekst, src, self.tt(thread_type))
		)
		self.need_commit = True

	def add_naklejka(self, ts, nadawca, adresat, sticker_id, url, src, thread_type):
		cursor = self.con.cursor()
		cursor.execute(
			"INSERT INTO naklejki VALUES (?,?,?,?,?,?,?)", 
			(ts, nadawca, adresat, sticker_id, url, src, self.tt(thread_type))
		)
		self.need_commit = True

	def add_obrazek(self, ts, nadawca, adresat, url, height, width, src, thread_type):
		cursor = self.con.cursor()
		cursor.execute(
			"INSERT INTO obrazki VALUES (?,?,?,?,?,?,?,?)", 
			(ts, nadawca, adresat, url, height, width, src, self.tt(thread_type))
		)
		self.need_commit = True

	def add_film(self, ts, nadawca, adresat, url, height, width, length, typ, rotation, src, thread_type):
		cursor = self.con.cursor()
		cursor.execute(
			"INSERT into filmy VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
			(ts, nadawca, adresat, url, height, width, length, typ, rotation, src, self.tt(thread_type))
		)
		self.need_commit = True

	def update_field(self, table, field, value, fb_id):
		cursor = self.con.cursor()
		cursor.execute("UPDATE {} SET {} = (?) WHERE fb_id = (?)".format(table, field), (value, fb_id))
		self.need_commit = True

	def check(self, fb_id):
		if fb_id in list(self.grupy_id.keys()):
			return 2
		if fb_id in self.uzytkownicy_id:
			return 1
		return 0

	def check_grupa_user(self, thread_id, author_id):
		users = self.grupy_id[thread_id]  # it must exist due to code flow
		if not author_id in users:  # its a string, seperated with commas
			self.grupy_id[thread_id] = users + ',' + author_id
			self.update_field('grupy', 'uzytkownicy_id', self.grupy_id[thread_id], str(thread_id))
			if self.callback.debug: print('Adding '+author_id+' to group '+thread_id)

class QueueEvent:
	def __init__(self, callback, func, *args):
		self.callback = callback
		self.func = func
		self.args = args

	def execute(self):
		self.func(self.callback, *self.args)

class FunctionsHolder:  # :v
	def __init__(self, callback, parser):
		self.callback = callback
		self.parser = parser

	def burze_polska(self, thread_id, thread_type):
		url_pl = 'http://burze.dzis.net/burze.gif'
		txt = 'Aktualny stan burz w Polsce (burze.dzis.net):'
		self.callback.queue.append(
			QueueEvent(self.callback, CustomClient.send_image_remote, url_pl, txt, thread_id, thread_type)
		)

	def meteogram(self, thread_id, thread_type):
		url_pl = 'http://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate={}&row=391&col=171&lang=pl'
		url_meteogram = 'http://new.meteo.pl/um/php/meteorogram_id_um.php?ntype=0u&id=2658'
		r = requests.get(url_meteogram)
		data = r.text.split('var fcstdate = "')[1].split('";')[0]
		url_pl = url_pl.format(data)
		print(url_pl)
		txt = 'Meteogram dla stacji Wronki (meteo.pl): '
		img = requests.get(url_pl)
		with open('temp/obrazek.png', 'wb') as f:
			if r.status_code == 200:
				for chunk in img:
					f.write(chunk)
		self.callback.queue.append(
			QueueEvent(self.callback, CustomClient.send_image_local, 'temp/obrazek.png', txt, thread_id, thread_type)
		)

	def pory_dnia(self, thread_id, thread_type):
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
		self.send_line(cool_text, thread_id, thread_type)	

	def change_color(self, message, thread_id, thread_type):
		split = message.split(' ')
		if len(split) >= 2:
			color = split[1]
		else:
			self.send_line('Należy zastosować komendę w formacie .kolor <kolor>!', thread_id, thread_type)
			return
		pattern = re.compile("^#(?:[0-9a-fA-F]{3}){2}$")
		if not pattern.match(color):
			self.send_line('Kolor musi być w formacie heksadecymalnym! (np. #AA13F8)', thread_id, thread_type)
			return
		class EksDee(Enum):
			col = color
		self.callback.queue.append(
			QueueEvent(self.callback, CustomClient.change_color, EksDee.col, thread_id)
		)


	def send_multiline(self, text_array, thread_id, thread_type):
		for line in text_array:
			self.callback.queue.append(
				QueueEvent(self.callback, CustomClient.send_text, line, thread_id, thread_type)
			)

	def send_line(self, text, thread_id, thread_type):
		self.callback.queue.append(
			QueueEvent(self.callback, CustomClient.send_text, text, thread_id, thread_type)
		)

	def exit_bot(self, thread_id, thread_type):
		self.callback.sendMessage('K', thread_id=thread_id, thread_type=thread_type)
		self.callback.logout()
		sys.exit()

class MessageParser:
	def __init__(self, callback):
		self.callback = callback
		self.functions_holder = FunctionsHolder(callback, self)
		self.logger = self.callback.logger

	def parse(self, message, author_id, thread_id, thread_type, ts, metadata, msg, self_sent):
		attach = msg['delta']['attachments']
		if attach:
			attach_type = attach[0]['mercury']['attach_type']
			if attach_type in ('photo', 'animated_image'):
				if message:
					self.logger.log_message(
						message, author_id, thread_id, thread_type, ts, metadata, msg)
					if not self_sent: 
						self.parse_message(
							message, author_id, thread_id, thread_type, ts, metadata, msg)
				_filename = attach[0]['filename']
				_url = attach[0]['mercury']['preview_url']
				_height = attach[0]['imageMetadata']['height']
				_width = attach[0]['imageMetadata']['width']
				self.logger.log_image(
					_filename, _url, _height, _width, author_id, thread_id, thread_type, metadata, ts)
				if not self_sent:
					self.parse_image(
						_filename, _url, _height, _width, author_id, thread_id, thread_type, metadata, ts)

			elif attach_type == 'sticker':
				_stickerID = attach[0]['mercury']['metadata']['stickerID']
				_url = attach[0]['mercury']['url']
				self.logger.log_sticker(
					_stickerID, _url, author_id, thread_id, thread_type, metadata, msg, ts)
				if not self_sent: 
					self.parse_sticker(
						_stickerID, _url, author_id, thread_id, thread_type, metadata, msg, ts)

			elif attach_type == 'video':
				_name = attach[0]['mercury']['name']
				_url = attach[0]['mercury']['url']
				_previewIMG = attach[0]['mercury']['metadata']['inbox_preview']
				_height = attach[0]['imageMetadata']['height']
				_width = attach[0]['imageMetadata']['width']
				_length = attach[0]['genericMetadata']['videoLength']
				_type = attach[0]['genericMetadata']['videoType']
				_rotation = attach[0]['genericMetadata']['videoRotation']
				self.logger.log_video(
					_name, _url, _height, _width, _length, _type, _rotation,
					author_id, thread_id, thread_type, metadata, msg, ts)
				if not self_sent:
					self.parse_video(
						_name, _url, _previewIMG, _height, _width, _length, _type, _rotation,
						author_id, thread_id, thread_type, metadata, msg, ts)

			elif attach_type == 'share':  # ignore - not worth
				pass

			elif attach_type == 'template':  # even more not worth
				pass

			else:
				print('!!!!!!!! NEW ATTACH_TYPE !!!!!!!!!')
				print(attach_type)
				print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

		else:
			self.logger.log_message(message, author_id, thread_id, thread_type, ts, metadata, msg)
			if not self_sent: self.parse_message(message, author_id, thread_id, thread_type, ts, metadata, msg)			
		
	def parse_message(self, message, author_id, thread_id, thread_type, ts, metadata, msg):
		owner_sent = str(author_id) in self.callback.owner_ids
		command = ''
		if message[0] == '.':
			_t = message.split(' ')
			if _t:
				command = _t[0]
		if not command: return

		if command in ('.end', '.quit', '.exit') and owner_sent:
			self.functions_holder.exit_bot(thread_id, thread_type)
		if command == '.burze':
			threading.Thread(target=self.functions_holder.burze_polska, args=(thread_id, thread_type)).start()
		if command in ('.pogoda', '.meteogram'):
			threading.Thread(target=self.functions_holder.meteogram, args=(thread_id, thread_type)).start()
		if command in ('.color', '.kolor'):
			threading.Thread(target=self.functions_holder.change_color, args=(message, thread_id, thread_type)).start()
		if command in ('.dzien', '.dzień', '.pory', '.fazy', '.goldenhour', '.wschód', '.wschod', '.zachod', '.zachód'):
			threading.Thread(target=self.functions_holder.pory_dnia, args=(thread_id, thread_type)).start()

	def parse_image(self, filename, url, height, width, author_id, thread_id, thread_type, metadata, ts):
		"""cool_text = 'Wysłano obrazek przez '+str(author_id)+' do '+str(thread_id)+'.\n'
		cool_text += 'Wymiary: ['+str(width)+'*'+str(height)+'], filename: '+filename+'.\n'
		source_msg = ''
		for tag in metadata['tags']:
			if 'source:' in tag: source_msg = tag
		komorka = 'komórki' if source_msg in ('source:chat:orca', 'source:titan:orca', 'source:titan:m_zero') else 'komputera'
		cool_text += 'Zdjęcie wysłano z '+komorka+' - metadata wskazuje na '+source_msg
		self.functions_holder.send_line(cool_text, thread_id, thread_type)"""
		pass

	def parse_sticker(self, stickerID, url, author_id, thread_id, thread_type, metadata, msg, ts):
		"""cool_text = 'Wysłano naklejkę przez '+str(author_id)+' do '+str(thread_id)+'.\n'
		cool_text = 'ID naklejki to '+str(stickerID)+'. URL - '+url+'\n'
		for tag in metadata['tags']:
			if 'source:' in tag: source_msg = tag
		komorka = 'komórki' if source_msg in ('source:chat:orca', 'source:titan:orca', 'source:titan:m_zero') else 'komputera'
		cool_text += 'Naklejkę wysłano z '+komorka+' - metadata wskazuje na '+source_msg
		self.functions_holder.send_line(cool_text, thread_id, thread_type)"""
		pass

	def parse_video(self, name, url, previewIMG, height, width, length, type, rotation, 
					author_id, thread_id, thread_type, metadata, msg, ts):
		"""cool_text = 'Wysłano film, ale jest tyle zmiennych że nie chce mi sie przetwarzac.'
		self.functions_holder.send_line(cool_text, thread_id, thread_type)"""
		pass

class Logger:
	def __init__(self, callback):
		self.callback = callback
		self.database_handler = DatabaseHandler(callback.db_name, callback)

	def log_message(self, message, author_id, thread_id, thread_type, ts, metadata, msg):
		source_msg = ''
		for tag in metadata['tags']:
			if 'source:' in tag:
				source_msg = tag
				break
		self.log_generic(author_id, thread_id, thread_type)
		self.database_handler.add_wiadomosc(int(ts), author_id, thread_id, message, source_msg, thread_type)
		if self.callback.debug: print(str(ts) + ' - '+source_msg+' - '+str(author_id)+' ['+str(thread_id)+'] - '+message)

	def log_image(self, filename, url, height, width, author_id, thread_id, thread_type, metadata, ts):
		cool_text = 'Wysłano obrazek przez '+str(author_id)+' do '+str(thread_id)+'.\n'
		cool_text += 'Wymiary: ['+str(width)+'*'+str(height)+'], filename: '+filename
		if self.callback.debug: print(cool_text)

		source_msg = ''
		for tag in metadata['tags']:
			if 'source:' in tag:
				source_msg = tag
				break
		self.log_generic(author_id, thread_id, thread_type)
		self.database_handler.add_obrazek(int(ts), author_id, thread_id, url, height, width, source_msg, thread_type)

	def log_sticker(self, stickerID, url, author_id, thread_id, thread_type, metadata, msg, ts):
		cool_text = 'Wysłano naklejkę przez '+str(author_id)+' do '+str(thread_id)+'.\n'
		cool_text = 'ID naklejki to '+str(stickerID)+'. URL - '+url+'\n'
		if self.callback.debug: print(cool_text)

		source_msg = ''
		for tag in metadata['tags']:
			if 'source:' in tag:
				source_msg = tag
				break
		self.log_generic(author_id, thread_id, thread_type)
		self.database_handler.add_naklejka(int(ts), author_id, thread_id, stickerID, url, source_msg, thread_type)

	def log_video(self, name, url, height, width, length, typ, rotation, 
					author_id, thread_id, thread_type, metadata, msg, ts):
		cool_text = 'Wysłano film, ale jest tyle zmiennych że nie chce mi sie przetwarzac.'
		if self.callback.debug: print(cool_text)

		source_msg = ''
		for tag in metadata['tags']:
			if 'source:' in tag:
				source_msg = tag
				break
		self.log_generic(author_id, thread_id, thread_type)
		self.database_handler.add_film(
			int(ts), author_id, thread_id, url, height, width, length, typ, rotation, source_msg, thread_type)

	def log_generic(self, author_id, thread_id, thread_type):
		if thread_type == ThreadType.GROUP:
			if not self.database_handler.check(thread_id):
				self.database_handler.add_grupa(thread_id, '', author_id)
				print('Nowa grupa dodana - '+thread_id)
			self.database_handler.check_grupa_user(thread_id, author_id)
		if not self.database_handler.check(author_id):
			self.database_handler.add_uzytkownik(author_id, '', '')
			print('Nowy uzytkownik dodany - '+author_id)	

class QueueHandler:
	def __init__(self, callback):
		self.callback = callback
		self.killed = False

	def run(self):
		while True:
			if self.killed:
				break
			if self.callback.queue:
				element = self.callback.queue.pop(0)
				element.execute()
				print('Executed element!')
			time.sleep(self.callback.queue_delay)

class ConfigReader:
	def __init__(self, config_name):
		self.config_name = config_name
		self.parser = configparser.ConfigParser()
		self.parser.read(self.config_name)
	
	def get_dict(self):
		return self.parser

class CustomClient(Client):
	def initialize(self, config_dict={}):  # i dont want to overwrite __init__
		self.queue = []
		self.queue_delay = float(config_dict['Delays']['queue_delay'])  # in seconds
		self.db_save_delay = float(config_dict['Delays']['db_save_delay'])
		self.db_name = str(config_dict['Other']['db_name'])
		self.debug = int(config_dict['Other']['debug'])
		self.id = str(config_dict['Other']['bot_id'])
		self.owner_ids = str(config_dict['Other']['owner_ids']).split(',')
		self.logger = Logger(self)
		self.message_parser = MessageParser(self)
		self.queue_handler = QueueHandler(self)

	def run(self):
		self.queue_thread = threading.Thread(target=self.queue_handler.run)
		self.db_thread = threading.Thread(target=self.logger.database_handler.run)

		self.queue_thread.start()
		self.db_thread.start()
		self.listen()

	def onMessage(self, message, author_id, thread_id, thread_type, ts, metadata, msg, **kwargs):
		self_sent = str(author_id) == self.id
		self.message_parser.parse(message, author_id, thread_id, thread_type, ts, metadata, msg, self_sent)

	def onColorChange(self, mid, author_id, new_color, thread_id, thread_type, ts, metadata, msg, **kwargs):
		pass

	def onEmojiChange(self, mid, author_id, new_emoji, thread_id, thread_type, ts, metadata, msg, **kwargs):
		pass

	def send_text(self, text, thread_id, thread_type):  # no keyword args
		self.sendMessage(text, thread_id=thread_id, thread_type=thread_type)

	def send_image_remote(self, url, message, thread_id, thread_type):
		self.sendRemoteImage(url, message=message, thread_id=thread_id, thread_type=thread_type)

	def send_image_local(self, path, message, thread_id, thread_type):
		self.sendLocalImage(path, message=message, thread_id=thread_id, thread_type=thread_type)

	def change_color(self, color, thread_id):
		self.changeThreadColor(color, thread_id=thread_id)

cr = ConfigReader('config.ini')
d = cr.get_dict()
client = CustomClient(d['Credentials']['email'], d['Credentials']['password'])
client.initialize(d)

try:
	client.run()
except (KeyboardInterrupt, SystemExit):
	client.logout()
	client.queue_handler.killed = True
	client.logger.database_handler.killed = True
	print('Goodbye!')
	sys.exit()
