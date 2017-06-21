from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import ngrams
import string, os, math

class Preprocessor:
	""" Class for extracting all the keywords.
	
		For extracting the keywords, various steps like tokenization, n-grams, stemming and stopwords removal are applied. The constructor takes in the list of files to extract keywords from.
	"""
	def __init__(self, files):
		self.files = files
		self.keywords = list()
		self.vector = {}
		self.stemmer = SnowballStemmer("english")
		self.stopwords = [str(word) for word in stopwords.words("english")]
	
	def extract(self):
		""" Method to extract all the tokens from documents.
		
			The process involves tokenizing the documents followed by 3-grams, stopwords removal, stemming.
		"""
		for file_ in self.files:
			data = open("Data/"+file_,"r").read()
			# print file_
			replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
			data = data.translate(replace_punctuation).lower()
			tokens =  wordpunct_tokenize(data)
			tokens = [word for word in tokens if len(word) > 1]
			# applying n-grams and removal of stopwords
			tokens2 = [' '.join(word) for word in ngrams(tokens, 2)]
			tokens3 = [' '.join(word) for word in ngrams(tokens, 3)]
			tokens = [word for word in tokens if word not in self.stopwords]
			# print tokens[:100]
			stemmedData = list()
			for word in tokens:
				try:
					stemmedData.append(str(self.stemmer.stem(word)))
				except Exception:
					pass
			stemmedData = stemmedData + tokens2+tokens3
			stemmedData = list(set(stemmedData))
			self.keywords += stemmedData
		self.keywords = list(set(self.keywords))

	def dumpKeywords(self):
		""" Method to dump all the keywords in a file named 'keywords.txt'.
		
			In this, tokens are separed by '_' so that they can recovered later easily.
		"""
		targetFile = open("keywords.txt","w")
		targetFile.write('_'.join(self.keywords))


		

class Classifier:
	""" The Classifier class which takes in the input sentence to be classified and classifies it among the training documents.
	
		inp  : input sentence
		files: list of training files
	
	"""
	def __init__(self, files):
		self.inp = raw_input()
		self.files = files
		self.stemmer = SnowballStemmer("english")
		self.stopwords = [str(word) for word in stopwords.words("english")]
		# print self.inp
	
	def classify(self):
		""" The main method that does the task of classifying input.
		
			It also tags the words that are being classified. Also, it adds the sentence to a file 'dtrain.txt' if unclassified so that model is updated dynamically later.
		
		"""
		replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
		self.inp = self.inp.translate(replace_punctuation).lower()
		tokens = wordpunct_tokenize(self.inp)
		tokens = [word for word in tokens if len(word) > 1]
		tokens2 = [' '.join(word) for word in ngrams(tokens, 2)]
		tokens3 = [' '.join(word) for word in ngrams(tokens, 3)]
		# print tokens
		tokens = [word for word in tokens if word not in self.stopwords]
		stemmedData = list()
		for word in tokens:
			try:
				stemmedData.append(str(self.stemmer.stem(word)))
			except Exception:
				pass
		stemmedData = stemmedData + tokens2+tokens3
		#print stemmedData
		vec = dict()
		f_later = dict()
		for ele in stemmedData:
			f_later[ele] = ''
			if ele in vec:
				vec[ele] += 1
			else:
				vec[ele] = 1
		#print vec
		score = [0]*8
		for docNum in range(1,9):
			tfidfVector = open("Tfidf/D" + str(self.files[docNum-1])).read().split('^')
			# print tfidfVector
			#print "Tfidf/D" + str(self.files[docNum-1]),
			final_vector = dict()
			for ele in tfidfVector:
				try:
					key, value = ele.split(':')
					final_vector[key] = float(value)
				except Exception:
					pass
			# print final_vector
			for ele in vec:
				try:
					score[docNum-1] += vec[ele]*final_vector[ele]
					f_later[ele] += str(docNum) + ','
					#print ele, vec[ele], final_vector[ele],
				except:
					pass
			#print docNum, score[docNum-1]
		#print score
		nd = sorted(range(len(score)), key=lambda i: score[i])[:]
		#print self.files
		#print nd
		fnd = [self.files[i] for i in nd]
		#print fnd
		for ele in f_later:
			f_later[ele] = f_later[ele][:-1].split(',')
		count = 1
		for ele in f_later:
			if '' in f_later[ele]:
				count = 0
		
		temp = f_later.copy()
		
		for it in range(-1,-9,-1):
			print "\n"
			if score[nd[it]] > 0:
				print "Class : D" + str(nd[it] + 1) + " (" + self.files[nd[it]][:-4] + ")"
				print "Score : " + str(score[nd[it]])
				print "Classifying words: "
				for key in temp:
					 if str(nd[it]+1) in temp[key]:
					 	print key
					 	temp[key] = ''

		if count == 0:
			train = open("dtrain.txt", "a")
			sentence = self.inp + "$" + str(nd[-1]) + "$"
			train.write(sentence)
			print sentence
	
if __name__ == '__main__':
	docs = os.listdir(os.getcwd()+'/Data/')
	p = Preprocessor(docs)
