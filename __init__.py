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
		
if __name__ == '__main__':
	docs = os.listdir(os.getcwd()+'/Data/')
	p = Preprocessor(docs)
