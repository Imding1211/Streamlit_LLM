
import json

#=============================================================================#

class SettingController():

	def __init__(self):

		self.default_setting = {
		    "llm_model": "gemma2:2b",
		    "base_url": "http://localhost:11434"
		}

		self.load_setting()

#-----------------------------------------------------------------------------#

	def load_setting(self):
		with open('setting.json', 'r', encoding='utf-8') as setting_file:
		    self.setting = json.load(setting_file)

#-----------------------------------------------------------------------------#

	def generate_setting(self, new_setting):
		with open('setting.json', 'w', encoding='utf-8') as setting_file:
			setting_file.write(json.dumps(new_setting, indent=4, ensure_ascii=False))

#-----------------------------------------------------------------------------#

	def generate_default_setting(self):
		with open('setting.json', 'w', encoding='utf-8') as setting_file:
			setting_file.write(json.dumps(self.default_setting, indent=4, ensure_ascii=False))

#-----------------------------------------------------------------------------#

	def change_llm_model(self, model_name):

		if len(model_name) > 0:

			self.setting['llm_model'] = model_name

			self.generate_setting(self.setting)

#-----------------------------------------------------------------------------#

	def change_base_url(self, base_url):

		self.setting['base_url'] = base_url

		self.generate_setting(self.setting)

#-----------------------------------------------------------------------------#

	def add_llm_model(self, model_name):

		pass

#-----------------------------------------------------------------------------#

	def remove_llm_model(self, model_name):

		pass
