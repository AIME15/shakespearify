#tester.py

import random, math
from string import ascii_lowercase
from author import authors

MAX_WORDS_PER_FILE = 1000000
MAX_TRAIN = 100000
MAX_TEST = 1000

sent_ind = 0
#files = dict ()
sentences = []

word_list = ['']
word_map = dict ()

def clean (word):
	word = word.lower ()
	ret = ""
	for c in word:
		if c in ascii_lowercase:# or c == '':
			ret = ret + c
	return ret

#open files
#read 
def read_input ():
	global word_list, word_map, sentences

	for author in authors:
		#files [author] = open ('../data/' + author,'r')
		wordfile = open ('../data/' + author + '.txt','r')
		numwords = 0
		words = []

		for line in wordfile:
			if numwords >= MAX_WORDS_PER_FILE:
				break

			cur_words = line.split ()
			for word in cur_words:
				if (word [len (word) - 1] == '.'):
					if (len (words) > 0):
						sentences.append ([words, author])
						numwords += len (words)
						words = []
				word_clean = clean (word.lower ())
				if len (word_clean) > 0:
					if word_clean not in word_map:
						word_map [word_clean] = len (word_list) 
						word_list.append (word_clean)
						assert (word_list[word_map[word_clean]] == word_clean)

					words.append (word_clean)
		print "Inputted", author + ";", numwords, "total words"
	random.shuffle (sentences)

def get_train ():
	global sent_ind, sentences

	sent_ind = (sent_ind + 1) % MAX_TRAIN
	return sentences [sent_ind]

def run_tests (predictor):
	global sent_ind, sentences

	correct = 0
	total = 0
	
	for i in range (MAX_TRAIN, MAX_TRAIN + MAX_TEST):
		ret = predictor (sentences[i][0])
		if ret == sentences [i][1]:
			correct += 1
		total += 1
		if (i % 10 == 9):
			print str(100.0 * correct/total) +'%', str(correct) + '/' + str(total)
