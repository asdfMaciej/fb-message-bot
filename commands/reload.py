from run_bot import CustomClient, QueueEvent, FunctionsHolder


class Command:
	command_names = [
		'.reload', '.restart', '.load'
	]
	admin_only = True
	description = "Ładuje komendy na nowo."

	@staticmethod
	def run(self, params_d):
		params_d['callback'].queue.append(
			QueueEvent(
				params_d['functions_holder'], FunctionsHolder.init_commands, 
				params_d['functions_holder'].folder
			)
		)
		
