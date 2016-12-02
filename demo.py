import markov
import script_reader
import random

def main():
	reader = script_reader.Script_Reader()
	actor_list = reader.get_list_of_actors()
	print("----Actors----")
	[print(actor) for actor in actor_list]

	selected_actors = ['Arthur', 'Martin', 'Douglas', 'Carolyn']
	models = {actor: create_markov_model(reader, actor) for actor in selected_actors}

	print("----Generated Lines----")
	[print("%s: %s" % (actor, models[actor].generate_sentence())) for actor in selected_actors]


def create_markov_model(reader, name):
	return markov.Text(reader.get_scripts_by_actor(name))

if __name__ == '__main__':
	main()