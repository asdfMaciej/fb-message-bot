from enum import Enum
import re
from run_bot import CustomClient, QueueEvent


class Command:
	command_names = [
		'.color', '.kolor'
	]
	admin_only = False
	description = "Zmienia kolor konwersacji, np. .kolor #1AB3F5"

	@staticmethod
	def run(self, params_d):
		split = params_d['message'].split(' ')
		if len(split) >= 2:
			color = split[1]
		else:
			params_d['functions_holder']._send_line(
				'Należy zastosować komendę w formacie .kolor <kolor>!', 
				params_d['thread_id'], params_d['thread_type']
			)
			return
		pattern = re.compile("^#(?:[0-9a-fA-F]{3}){2}$")
		if not pattern.match(color):
			params_d['functions_holder']._send_line(
				'Kolor musi być w formacie heksadecymalnym! (np. #AA13F8)',
				params_d['thread_id'], params_d['thread_type']
			)
			return
		class EksDee(Enum):
			col = color
		params_d['callback'].queue.append(
			QueueEvent(
				params_d['callback'], CustomClient.change_color, EksDee.col, params_d['thread_id']
			)
		)
