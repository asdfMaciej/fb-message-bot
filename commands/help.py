class Command:
	command_names = [
		'.help', '.komendy', '.pomoc', '.halp', '.?'
	]
	admin_only = False
	description = "Pokazuje listę komend."

	@staticmethod
	def run(self, params_d):
		dic = params_d['functions_holder'].commands
		ret_str = "["
		for komenda in dic:
			ret_str += '/'.join(komenda[0])+'] '
			if komenda[1]: ret_str += '[Adm] '
			ret_str += " - " + komenda[2] + "\n["
		ret_str = ret_str[:-1]
		params_d['functions_holder']._send_line(
			ret_str, params_d['thread_id'], params_d['thread_type']
		)
