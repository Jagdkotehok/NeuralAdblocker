from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import sklearn.metrics as skm
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
from pymystem3 import Mystem
import glob
from parse_train import ParseTrain
import time


nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))
parsing = {}
m = Mystem()
tokenizer = RegexpTokenizer(r'[а-яА-Я]+')


class NeuroSearch:
	"""
	Класс проверяет субтитры на рекламу.
	
	Поля класса:
	vectorizer -- создаёт мешок слов.
	x_data -- обучающие данные.
	y_data -- обучающие ответы.
	x_train -- тренировочные данные.
	y_train -- тренировочные ответы.
	x_test -- тестовые данные.
	y_test -- тестовые ответы.
	"""
	def  __init__(self):
		"""Конструктор."""
		self.vectorizer = CountVectorizer()
	
	
	def load(self):
		"""Загрузка модели."""
		data = self.load_result() # data[0] -> test, data[1] -> answer
		self.x_data = self.vectorizer.fit_transform(data[0])
		self.y_data = data[1]
		self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x_data, self.y_data, test_size=0.33, random_state=42)
		self.clf = LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced').fit(self.x_train, self.y_train)
	
	
	def load_result(self):
		""""Загрузка готовых данных."""
		files = glob.glob("./ans/*.txt")
		data = [[], []]
		for now in files:
			print(now)
			res = ParseTrain(now).parse_result()
			if res == None:
				continue
			data[0].extend(res[0])
			data[1].extend(res[1])
		return data
	
	
	def load_data_set(self):
		"""Загрузка данных для разбиения."""
		files = glob.glob('./res/*.xml')
		ind = -520
		for now in files[-520::-1]:
			result1 = []
			result2 = []
			string = now[6:-4]
			print('Parse : ' + now)
			print(ind)
			ind -= 1
			data = ParseTrain(now).parse_data_set()
			text = []
			for index in range(len(data[0])):
				line_now = self.preprocess_dataset(data[0][index])
				text.append(line_now)
				result2.append(data[1][index])
			text = self.process_dataset(text)
			with open('ans/' + string + '_1.txt', 'w', encoding='UTF-8') as f:
				f.write(str(text))
			with open('ans/' + string + '_2.txt', 'w', encoding='UTF-8') as f:
				f.write(str(result2))
		print(len(result1))
		return [result1, result2]
	
	
	def preprocess_dataset(self, data):
		"""Удаление плохих слов."""
		return [token for token in tokenizer.tokenize(data.lower()) if token not in stop_words]
	
	
	def process_dataset(self, data):
		"""Удаление форм слов."""
		length = [len(x) for x in data]
		text = [' '.join(x) for x in data]
		text = ' '.join(text)
		res = m.lemmatize(text) 
		res2 = []
		for i in range(len(res)):
			if i % 2 == 0:
				res2.append(res[i])
		res3 = [[] for _ in range(len(length))]
		index = 0
		for now in res2:
			while (len(res3[index]) == length[index]):
				index += 1
			res3[index].append(now)
		res3 = [' '.join(now) for now in res3]
		return res3
	
	
	def evaluate(self):
		"""Качество модели."""
		predictions = self.clf.predict(self.x_test)
		labels = self.y_test
		print("Accuracy {:.3f}".format(skm.accuracy_score(labels, predictions)))
		print("Precision {:.3f}".format(skm.precision_score(labels, predictions)))
		print("Recall {:.3f}".format(skm.recall_score(labels, predictions)))
