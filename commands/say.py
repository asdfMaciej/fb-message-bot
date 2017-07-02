class Command:
	command_names = [
		'.say'
	]
	admin_only = False
	description = "Mówi coś w imieniu bota - .say wiadomość"

	@staticmethod
	def run(self, params_d):
		split = params_d['message'].split(' ')
		if len(split) >= 2:
			wiadomosc = ' '.join(split[1:])
		else:
			params_d['functions_holder']._send_line(
				'Należy zastosować komendę w formacie .say <wiadomość>!', 
				params_d['thread_id'], params_d['thread_type']
			)
			return
		params_d['functions_holder']._send_line(
			wiadomosc, params_d['thread_id'], params_d['thread_type'])