import pandas as pd
import numpy as np
from sklearn import datasets, svm, cross_validation
import sys
sys.path.append("..")
import re
from sklearn.feature_extraction.text import CountVectorizer
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords 
from sklearn.ensemble import RandomForestClassifier
from goose import Goose
from requests import get  
from bs4 import BeautifulSoup
import urllib2




file_name = './data/fake.csv'
test_file = './data/test.csv'


def HTMLParser(url):
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    content = page.read()
    page.close()  
    soup = BeautifulSoup(content) 
    return soup




def clean(s):
	letters_only = re.sub("[^a-zA-Z]", " ", s) 
	words = letters_only.lower().split()
	stops = set(stopwords.words("english"))
	meaningful_words = [w for w in words if not w in stops]
	return( " ".join( meaningful_words ))



def read():
	
	global df
	
	df = pd.read_csv(file_name)	
	
	df_goal = df['type']
	df["text"].fillna(" ",inplace=True)  
	df["type"].fillna(" ",inplace=True)  
	df["text"] =df["text"].apply(clean)
	df["type"] =df["type"].apply(clean)


	df = df[df['type'].isin(['bias', 'fake', 'conspiracy', 'real'])]
	
	global input
	df['text'] = df['text'].str.replace(r'[^\w]', ' ')



def train():


	
	read()
	preds = []
	global v
	v = CountVectorizer(ngram_range=(1,3), stop_words='english')
	
	
	
	
	X = v.fit_transform(df['text'].values)
	y = df['type']
	
	#logreg = linear_model.LogisticRegression(C=1, penalty='l1')
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)
	
	


	'''
	model = logreg.fit(X_train, y_train)
	df_test = pd.read_csv(test_file, skiprows = 0)	




	df_test2 = pd.read_csv(file_name, skiprows = 0, nrows=20, usecols=['type', 'text'])	
	X_test=v.transform(df_test['text'].values)
	X_test_2=v.transform(df_test2['text'].values)


	print df_test2

	df_test = pd.read_csv(test_file, skiprows = 0)
	
	
	prediction = model.predict_proba(X_test)
	print prediction

	prediction = model.predict_proba(X_test_2)
	print prediction
	
	'''



	
	#df_test = pd.read_csv(test_file, skiprows = 0)
	#print df_test	
	
	#print df_test
	

	
	
	
	global forest
	forest = RandomForestClassifier(n_estimators = 100) 
	forest = forest.fit(X_train, y_train)


def compute(url):
	'''
	train()
	'''
	text = HTMLParser(url)
	print type(str(text))
	exit()
	data = {'text': [text]}

	df_test = pd.DataFrame.from_dict(data)
	
	print df_test["text"]

	exit()
	df["text"] =df["text"].apply(clean)

	'''
	X_test=v.transform(df_test['text'].values)
	prediction = forest.predict(X_test)
	print prediction
	prediction = forest.predict_proba(X_test)
	print prediction
	'''

compute("http://www.cnbc.com/2017/02/18/heres-how-congress-is-handling-russia-investigations.html")

