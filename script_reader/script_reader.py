from os import listdir, getcwd
from os.path import isfile, join
import re
from unidecode import unidecode


class Script_Reader:
	def __init__(self, folder_path = 'transcripts'):
		files = [join(folder_path, file) for file in listdir(folder_path) if isfile(join(folder_path, file))]
		self.scripts = self.extract_lines_by_actor(files)

	def extract_lines_by_actor(self, files):
		actor_scripts= {}
		for file in files:
			with open(file, encoding = 'utf-8') as text:
				for line in text:
					line = unidecode(line)
					if len(line.split(": ", 1)) == 2:
						[name, script] = line.split(":", 1)
						name = re.sub(r'\([^)]+\)',"", name.casefold().lstrip())
						script = re.sub(r'\([^)]+\)|\n', " ", script)

						if name.find(" and ") != -1:
							name = re.sub(r', ', " and ", name)
							name_array = name.split(" and ")
						else:
							name_array = [name]

						for each_name in name_array:
							each_name = each_name.rstrip()
							if each_name not in actor_scripts:
								actor_scripts[each_name] = script
							else:
								actor_scripts[each_name] +=script
		# [print(name) for name in actor_scripts]
		return actor_scripts

	def get_scripts_by_actor(self, actor_name):
		if actor_name.casefold() not in self.scripts.keys():
			print("%s not found", actor_name)
			return ""
		return self.scripts[actor_name.casefold()]

	def get_list_of_actors(self):
		return self.scripts.keys()