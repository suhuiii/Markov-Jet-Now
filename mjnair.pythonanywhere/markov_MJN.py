import transcripts
import MarkovMe
from transcripts import Transcript

class markov_MJN:
	def __init__(self, name_list):
		self.models = {name: self.create_dictonary(name) for name in name_list}

	def create_dictonary(self, name):
		return self.create_markov_model(name)

	def create_markov_model(self, name):
		transcripts = Transcript()
		return MarkovMe.Text(transcripts.get_scripts_by_actor(name), False, 3)

	def getModel(self, name):
		return self.models[name]