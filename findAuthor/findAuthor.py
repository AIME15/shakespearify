#findAuthor.py

from math import log, sqrt
from tester import read_input,get_train, run_tests, authors, MAX_TRAIN, word_list, word_map, clean
import numpy
import interpret

EPOCHS = 1
NUM_AUTHORS = len (authors)
EPS = 1E-2

NUM_WORDS = None
N = None
W = None
alpha = 0.00001

freq = dict()
word_count = dict()

for author in authors:
	freq[author] = dict()

def mat_author(author):
	global authors

	for i in range (NUM_AUTHORS):
		if authors [i] == author:
			d = numpy.zeros((NUM_AUTHORS, 1)) 
			d[i, 0] = 100
			return numpy.mat (d)
	assert (False)

def get_feature_vector (sentence):
	global word_map, N

	X = numpy.zeros ((N, 1))
	#0th element is 1
	X [0, 0] = 1
	for word in sentence:
		if word in word_map:
			X [word_map[word], 0] += 1

    #use api stuff, except darn this doesn't really work
	#score = interpret.stringToSentiment(' '.join(sentence))
	#X [NUM_WORDS, 0] = score
	#X [NUM_WORDS, 0] = 0
	X [NUM_WORDS, 0] = len (sentence)

    #done
	return X

#useless stuff
def sq (a): 
	return a * a
def normalize ():
	global W
	for j in range (1,NUM_WORDS):
		var = 0.0
		for i in range (NUM_AUTHORS):
			var += sq (W [i,j])
		std = sqrt (var)
		assert (var > 0)
		for i in range (NUM_AUTHORS):
			W[i,j] /= std
def get_best (Y):
	global authors
	best = 0
	for i in range (NUM_AUTHORS):
		if Y[i, 0] > Y[best, 0]:
			best = i
	return authors [best]

def train_bayes():
	global MAX_TRAIN, freq, word_count

	example = get_train()
	num_iter = 0	
	while True:
		if num_iter >= MAX_TRAIN:
			break
		num_iter += 1

		[sentence, author] = example
		words = sentence
		for word in words:
			if word not in freq[author]: # this code is ugly
				freq[author][word] = 0
			freq[author][word] += 1

		example = get_train()

	for author in authors:
		word_count[author] = sum([freq[author][key] for key in freq[author]]) + 0.0

#set initial weights to naive bayes results
def setW():
	global W, NUM_AUTHORS, word_list, freq, word_count, authors

	for i in range (NUM_AUTHORS):
		for j in range(len(word_list)):
			if j == 0:
				continue
			word = word_list [j]
			author = authors [i]

			score = log (EPS) - log (word_count [author])
			if word in freq[author]:
				score = log(freq[author][word]) - log(word_count[author])
			W [i, j] = score

def train():
	global W,alpha, N, EPOCHS, MAX_TRAIN

	example = get_train()
    
	num_iter = 0
	num_cor = 0
	while True:
		if num_iter >= MAX_TRAIN * EPOCHS / 10:
			break
		num_iter += 1

		[sentence, author] = example
        
		x = numpy.mat (get_feature_vector (sentence))
		d = mat_author (author)
		Y = W * x
		W += alpha * (d - Y) * (x.transpose())
		
		"""
		dawg = get_best (Y)
		if get_best (Y) == author:
			num_cor += 1
			print dawg
		"""

		example = get_train()

def test(sentence):
	global W

	x = get_feature_vector (sentence)
	Y = W * x
	ret = get_best (Y)
	return ret

def test_string (s):
	sentence = []
	for word in s.split():
		sentence.append (clean (word))
	print sentence
	return test (sentence)

print "Reading Input..."
read_input ()
N = len (word_list) + 1 # size of feature vector
W = numpy.mat (numpy.zeros((NUM_AUTHORS, N)))
NUM_WORDS = len(word_list)

print "Training Bayes..."
train_bayes()
setW()
#print "Normalizing W"
#normalize ()
print "Training..."
train()

print test_string ("To be, or not to be")
print test_string ("Oh what a rouge and peasant slave am i")
print test_string ("Macbeth")

print "Testing..."
run_tests(test)
