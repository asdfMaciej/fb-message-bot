class Command:
	command_names = [
		'.ping'
	]
	admin_only = False
	description = "Pong!"

	@staticmethod
	def run(self, params_d):
		params_d['functions_holder']._send_line(
			'Pong!', params_d['thread_id'], params_d['thread_type'])
