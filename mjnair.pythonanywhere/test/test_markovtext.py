import MarkovMe
import os
import re

class TestMarkov:
	def setup_class(self):
		file = open(os.path.join(os.path.dirname(__file__),"text/theprince.txt"))
		self.test = MarkovMe.Text(file.read())
		
	def test_default_state_size_is_2(self):
		self.test = MarkovMe.Text("hello")
		assert "hello" == self.test.input_text
		assert 2  is self.test.state_size

	def test_generate_corpus(self):
		assert type(self.test.corpus) is list
		assert type(self.test.corpus[0]) is list

	def test_words_to_model(self):
		self.test = MarkovMe.Text("The quick brown fox jumps over the brown fox who is slow jumps over the brown fox who is dead.")
		keys = self.test.model.model.keys()
		assert ('brown', 'fox') in keys
		assert ('jumps') in self.test.model.model[('brown', 'fox')]
		assert (self.test.model.model[('brown', 'fox')]['jumps']) is 1
		assert ('who') in self.test.model.model[('brown', 'fox')]
		assert (self.test.model.model[('brown', 'fox')]['who']) is 2

	def test_generate_sentence(self):
		assert len(self.test.generate_sentence()) > 1
		assert type(self.test.generate_sentence()) is str

	def test_word_joiner(self):
		assert self.test.join_words(['are', 'you', 'there', 'yet?']) == "are you there yet?"

	def test_sentence_valid(self):
		assert self.test.sentence_valid("ok") is True
		assert self.test.sentence_valid("All states, all powers, that have held and hold rule over men have been".split()) is False
	