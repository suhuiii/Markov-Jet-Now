import re
from nltk.tokenize import wordpunct_tokenize, sent_tokenize
from unidecode import unidecode
from .Model import Model

punctuation = ",.!?;'-/):"
# no_space_punctuation = "':\\/-@#()_"a

class Text(object):

	def __init__(self, input_text, separated_by_newlines = False, state_size = 2, ):
		self.state_size = state_size
		self.separated_by_newlines = separated_by_newlines
		self.corpus = self.generate_corpus(input_text)
		self.model = Model(self.corpus, self.state_size)

	def remove_unicode_newlines_URLs_symbols(self, text):
		# decode to ASCII
		text = unidecode(text)
		# remove symbols that will otherwise be strange in randomly generated text
		text = re.sub(r"(^')|('$)|\"", "", text)
		return text

	def split_sentence(self, text):
		self.input_text = self.remove_unicode_newlines_URLs_symbols(text)
		clean_text = ""

		#use NLTK to tokenize each line
		if self.separated_by_newlines:
			return self.word_tokenizer(self.input_text.split("\n"))

		# removes extra newlines that are not related to sentence structure
		for line in self.input_text.split("\n"):
			clean_text += line.strip()+ " "

		#use NLTK to tokenize each sentence
		return self.word_tokenizer(sent_tokenize(clean_text))

	def word_tokenizer(self, text_list):
		return [words.split() for words in text_list]

	def generate_corpus(self, input_text):
		words = self.split_sentence(input_text)
		return list(filter(None, words))

	def generate_sentence(self, initial = None):
		words = []
		while True:
			words = self.model.run()
			if len(words) :
				if self.sentence_valid(words):
					break;
		return self.join_words(words)

	def sentence_valid(self, result):
		if self.join_words(result) in self.input_text:
				return False
		return True


	def join_words(self, words):
		return " ".join(words)

