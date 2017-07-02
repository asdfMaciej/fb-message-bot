from run_bot import CustomClient, QueueEvent


class Command:
	command_names = [
		'.burze', '.burza'
	]
	admin_only = False
	description = "Pokazuje stan burz w Polsce (burze.dzis.net)."

	@staticmethod
	def run(self, params_d):
		url_pl = 'http://burze.dzis.net/burze.gif'
		txt = 'Aktualny stan burz w Polsce (burze.dzis.net):'
		params_d['callback'].queue.append(
			QueueEvent(
				params_d['callback'], CustomClient.send_image_remote, url_pl, 
				txt, params_d['thread_id'], params_d['thread_type']
			)
		)
