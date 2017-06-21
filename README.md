# Text Classifier

#### Use Case   
The project's use case consists of training data from several unclassified text documents which contains data across various fields. Given a number of input sentences, we classify each sentence to one of the many documents. Also, we tag individual tokens of the sentence into appropriate documents. Further, for improving the training model when we encounter exceptional inputs, we update the training model dynamically.

## Project Documentation
There are various steps that our project can be divided into which are basically some of the most common techniques followed in a general text classfication problem. Following are the list of steps done:  
1. Extracting all text from the documents.
2. Tokenization
3. Application of N-Grams (N=3 in our case)
4. Removal of Stopwords
5. Stemming
6. Feature Transformation and Vectorization using TfIdf Metric
7. Prediction 

The main project file is *init.py* which consists of two main classes namely, the **Preprocessor** class and the **Classifier** class.

## Class Reference

### Preprocessor Class


**Methods**
* ```__init__(self, files)```
* ```extract(self)```
* ```dumpKeywords(self)```
* ```vectorize(self)```
* ```dumpVectors(self)```
* ```applyTfidf(self)```

**Description**  

The class is responsible for extracting all the keywords from all the training documents followed by the application of various text classification techniques on the data. Basically, The preprocessor class specifies all the preprocessing tasks needed to be done for training the text classification model before actual classification can be done.  

#### Method Documentation

1. **__ init __ (self, files)**  
The constructor method for creating a Preprocessor object. This takes only one argument as the list of training documents to be used in the model.

2. **extract(self)**  
This method is responsible for extracting all the tokens from each of the documents and storing them in *self.keywords* member variable. Before actually storing the keywords, preprocessing tasks like removing punctuations, n-grams, stopwords removal and stemming are done.

3. **dumpKeywords(self)**  
This is the Method to dump all the keywords in a file named 'keywords.txt'. Tokens are separated by an underscore and then stored in the file.

4. **vectorize(self)**  
This method is responsible for computing the feature vector. The vector is formed using a dictionary named *self.vector*, a member variable of the class which stores the count of all keywords across all documents.

5. **dumpKeywords(self)**  
This Method dumps the frequency vector in a file called *'total.txt'*.The method stores the key, value pairs in the file separated by '^' so that it can be read easily later.

6. **applyTfIdf(self)**  
The method does the task of feature transformation using a metric known as TfIdf and stores individually for each document the TfIdf vector in separate files in a folder called *Tfidf*. The terms mean the following:  
	+ **Tf** stands for Term frequency
	+ **Idf** stands for inverse document frequency 


### Classifier Class


**Methods**
* ```__ init __ (self, files, inp) ```
* ```classify (self)```  

**Description**  
The Classifier class is the main class responsible for the actual prediction or classification. The classification is done on the basis of a metric called *Cosine Similarity*. For each of the tokens in the input sentence received to be classified, tagging takes place to appropriate document from the training data.

#### Method Documentation

1. **__ init __(self, files, inp)**  
The constructor method for creating a classifier object. As an argument, it takes in the list of training files as *files* and the input sentence to be classified as the *inp*.

2. **classify(self)**  
This is the main method that does the task of classifying input into documents. First, tokenization, n-grams, stopwords removal and stemming are applied on the input sentence as the preprocessing step. Next, the sentence is classified into some document based on the results of cosine similarity with the documents. Finally, individual tokens of the sentence are tagged to the most appropriate document.  
There may come a case when the sentence is not classified at all in any of the classes. In this case, the method stores the sentence in a separate file called *dtrain.txt* so that later the training model is updated dynamically using this. Retraining can then be done.

___

**NOTE:**  
+ The training data contains only a few documents at present. This will be extended later for better results.
+ The next step of the project is to use pre-defined classifiers from Python libraries and observe the results.
