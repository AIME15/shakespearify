import random, math
from string import ascii_lowercase

authors = [
'aristotle',
'dickens',
'jefferson',
'kant',
'poe',
'shakespeare',
'sophocles',
'yudkowsky'
]

MAX_WORDS_PER_FILE = 10000000
MAX_TRAIN = 100000
MAX_TEST = 1000

sent_ind = 0
#files = dict ()
sentences = []

def clean (word):
	ret = ""
	for c in word:
		if c in ascii_lowercase or c == ',':
			ret = ret + c
	return ret

#open files
#read 
def read_input ():
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
					words.append (word_clean)
		print "Inputted", author, ";", numwords, "total words"
	random.shuffle (sentences)

def get_train ():
	global sent_ind, sentences

	if sent_ind >= MAX_TRAIN:
		return None
	sent_ind += 1
	return sentences [sent_ind]

def run_tests (predictor):
	global sent_ind, sentences
	
	correct = 0
	total = 0
	
	for i in range (MAX_TRAIN, MAX_TRAIN + MAX_TEST):
		ret = predictor (sentences[i][0])
		if ret == sentences [i][1]:
			correct += 1
		else:
			print sentences [i][0], sentences [i][1], ret
		total += 1
		if (i % 1000 == 999):
			print 100.0 * correct/total,'%', correct, '/', total
