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
			replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
			data = data.translate(replace_punctuation).lower()
			tokens =  wordpunct_tokenize(data)
			tokens = [word for word in tokens if len(word) > 1]
			# applying n-grams and removal of stopwords
			tokens2 = [' '.join(word) for word in ngrams(tokens, 2)]
			tokens3 = [' '.join(word) for word in ngrams(tokens, 3)]
			tokens = [word for word in tokens if word not in self.stopwords]
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

	def vectorize(self):
		""" Method to vectorize all the keywords.
		
			The vector is formed using a dictionary named vector which stores the count of all keywords.
		"""
		key_list = open("keywords.txt","r").read().split("_")
		for key in key_list:
			self.vector[key] = 0
		for file_ in self.files:
			data, stemmedData = open("Data/"+file_,"r").read(), list()
			replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
			data = data.translate(replace_punctuation).lower()
			tokens = wordpunct_tokenize(data)
			tokens = [word for word in tokens if len(word) > 1]
			# applying n-grams and removal of stopwords
			tokens2 = [' '.join(word) for word in ngrams(tokens, 2)]
			tokens3 = [' '.join(word) for word in ngrams(tokens, 3)]
			tokens = [word for word in tokens if word not in self.stopwords]
			for token in tokens:
				try:
					stemmedData.append(str(self.stemmer.stem(token)))
				except Exception:
					pass
			stemmedData = stemmedData + tokens2+tokens3
			for ele in stemmedData:
				self.vector[ele] += 1
	
	def dumpVector(self):
		""" Method to dump the frequency vector in a file called 'total.txt'.
		
			The method stores the key, value pairs in the file separated by '^' so that it can be read directly later.
		"""
		targetFile = open("Total.txt","w")
		for key in self.vector:
			value = key + ":" + str(self.vector[key]) + "^"
			targetFile.write(value)

	def applyTfIdf(self):
		""" Method to apply TfIdf technique and store the respective file vectors in separate files.
		
			Tf : Term Frequency
			Idf: Inverse Document Frequency
		"""
		inp_list = open("Total.txt","r").read().split("^")
		final_vector = dict()
		for ele in inp_list:
			try:
				key, value = ele.split(':')
				final_vector[key] = int(value)
			except:
				pass
		for file_ in self.files:
			data, vec = open("Data/"+file_,"r").read(), dict()
			replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
			data = data.translate(replace_punctuation).lower()
			tokens =  wordpunct_tokenize(data)
			tokens = [word for word in tokens if len(word) > 1]
			# applying n-grams and removal of stopwords
			tokens2 = [' '.join(word) for word in ngrams(tokens, 2)]
			tokens3 = [' '.join(word) for word in ngrams(tokens, 3)]
			tokens = [word for word in tokens if word not in self.stopwords]
			stemmedData = list()
			for word in tokens:
				try:
					stemmedData.append(str(self.stemmer.stem(word)))
				except Exception:
					pass
			stemmedData = stemmedData +tokens2+tokens3
			for token in stemmedData:
				if token in vec:
					vec[token] += 1
				else:
					vec[token] = 1
			for token in vec:
				vec[token] = (float(vec[token]))*(math.log(1+(8.0/final_vector[token])))
			fname = "Tfidf/D" + str(file_)
			fout = open(fname, "w")
			for key in vec:
				outStr = key + ":" + str(vec[key]) + "^"
				fout.write(outStr)


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
		tokens = [word for word in tokens if word not in self.stopwords]
		stemmedData = list()
		for word in tokens:
			try:
				stemmedData.append(str(self.stemmer.stem(word)))
			except Exception:
				pass
		stemmedData = stemmedData + tokens2+tokens3
		vec = dict()
		f_later = dict()
		for ele in stemmedData:
			f_later[ele] = ''
			if ele in vec:
				vec[ele] += 1
			else:
				vec[ele] = 1
		score = [0]*8
		for docNum in range(1,9):
			tfidfVector = open("Tfidf/D" + str(self.files[docNum-1])).read().split('^')
			final_vector = dict()
			for ele in tfidfVector:
				try:
					key, value = ele.split(':')
					final_vector[key] = float(value)
				except Exception:
					pass
			for ele in vec:
				try:
					score[docNum-1] += vec[ele]*final_vector[ele]
					f_later[ele] += str(docNum) + ','
				except:
					pass
		nd = sorted(range(len(score)), key=lambda i: score[i])[:]
		fnd = [self.files[i] for i in nd]
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
	#print docs
	p = Preprocessor(docs)
	#p.extract()
	#p.dumpKeywords()
	#p.vectorize()
	#p.dumpVector()
	#p.applyTfIdf()
	#print "done"
	c = Classifier(docs)
	c.classify()