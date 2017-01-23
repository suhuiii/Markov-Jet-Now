# Markov-Jet-Now: 
##*A Markov chain generator for TV scripts and screenplays*
This is a Markov chain generator written in Python that uses TV scripts and screenplays as its corpus. A Markov model can thus be generated for each character.

***Update Dec 2016:** By using this code in combination with Flask and some SQLite, [Markov-ing Cabin Pressure](http://mjnair.pythonanywhere.com/) is now live!*

##Background
[Cabin Pressure](http://www.bbc.co.uk/programmes/b00lmcxj) is one of my favorite radio shows of all time, and I thought it would be cool to generate Markov-Chains of each character on the show while learning python and picking up web development.

## Format of scripts and screen plays
**Note:** 
*This project assumes that the script is in the following format
```
<actor_1>:<text>
<actor_2>:<text>
...
<actor_n>:<text>
```
where the actor's name and his line is separated by a colon (optional spaces around the colon), and each line by different actors is separated by a newline.

Stand-alone lines which are not preceded by a name, as well as anything in parentheses is ignored.
```
DOUGLAS ~~(exasperated)~~: Ah, yes, of course. May. 
MARTIN: Mm-hm, yep. Cant.
~~(Flight deck door opens.) ~~
ARTHUR: Here we are, gents.
```
Scripts should be put in a folder named *transcripts* in the project root directory.

** Cabin Pressure Transcripts taken from [here](http://www.cabinpressurefans.co.uk/cabin-pressure-episode-transcripts/)

## Usage
This project consists of two modules that are independent of each other:

1. script_reader - reads scripts from a folder and generates a dictionary of key value pairs where
   *keys are the the actors in the transcripts, and
   *values are all the lines the actor has said in the scripts
2. Markov chain generator: given a corpus, generate a Markov model for the corpus

This allows the user to swap out the markov module for some other text generator of their choice.

Import the packages into your python code
`import script_reader`
`import markov`

### To use the script reader
**1. Creating a script reader object**

    If your scripts are in the default folder *transcripts*
        `reader = script_reader.Script_Reader() `
    Otherwise pass the folder path as a string 
        `reader = script_reader.Script_Reader('folder_path') `
    The reader will automatically read all the files in the folder.

**2. List all actors**

    To obtain the full list of actors that the reader has found
    `reader.get_list_of_actors()`

**3. Obtaining an actor's full script**

    To get all the lines that an actor has said:
    `reader.get_scripts_by_actor('<name>')`

### To use the Markov Chain Generator
**1. Create a Markov Chain object**

    Simply pass the corpus as a parameter to create a Markov Model with a state size of 2
    `model = markov.Text(corpus)`  
    You can adjust the state size by passing an additional parameter  
    `model = markov.Text(corpus, 3)`  

**2. Generate a sentence**

    A random sentence can be generated simply be executing  
    `model.generate_sentence()'  
    The model will only output a sentence if the exact sequence of words is not present in the corpus. The model will try up to 10x before giving up and outputting an empty string.

*Note that this particular Markov Chain generator is not a true probabilistic Markov Generator. Due to the small corpus size of the scripts I was working with, I have opted to choose the next state by:*

1. *generating up to 5 next-states based on their probability given the current state*

2. *then randomly choose one of the 5 choices as the next-state*

*This provides more variance in the random sentences generated.*

### Combined Use of Both Modules

A demonstration of the combined use of both modules can be found in demo.py

