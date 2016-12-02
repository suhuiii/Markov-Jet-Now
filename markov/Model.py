from itertools import accumulate
import random
import bisect

BEGIN = "___BEGIN__"
END = "___END__"

class Model(object):

	def __init__(self, corpus, state_size):
		self.state_size = state_size
		self.model = self.build(corpus, self.state_size)

	def build(self, corpus, state_size):
		model = {}

		for sentence in corpus:
			# add "begin" and "end" to delimit boundaries
			delimited_sentence = ([BEGIN] *state_size) + sentence + [END]

			for i in range(len(sentence) + 1):
				# split portions of sentence into key value pairs
				key = tuple(delimited_sentence[i : i + state_size]) 
				value = delimited_sentence[i + state_size]
				# count occurences of key value pairs
				if key not in model:
					model[key] = {} 
				if value not in model[key]:
					model[key][value] = 0
				model[key][value] += 1
		return model

	def generateText(self):
		currentstate = (BEGIN,) * self.state_size
		while True:
			# for _ in range(5):
			# 	print(self.get_next_word_from(currentstate))
			next_word = self.get_next_word_from(currentstate) #get next word based on current state
			if next_word == END:
				break
			yield next_word
			currentstate = tuple(currentstate[1:]) +(next_word,) #update current state

	def get_next_word_from(self, state):
		# get next word based on weights/occurences of key value pairs
		values, weights = zip(*self.model[state].items())
		# print(values)
		cumdist = list(accumulate(weights))
		arr = []
		for i in range(min(len(values),5)):
			random_value = random.random() * cumdist[-1]
			val = values[bisect.bisect(cumdist, random_value)]
			if val not in arr:
				arr.append(val)
		return random.choice(arr)

	def run(self):
		return list(self.generateText())