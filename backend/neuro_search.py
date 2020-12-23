from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from gensim.models import word2vec
import numpy as np
import sklearn.metrics as skm
from scipy.sparse import vstack
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
from pymystem3 import Mystem
import glob
from parse_train import ParseTrain
import time


"""


classifier = trainLogReg(transform_text([' '.join(x) for x in X_data]), Y_data)

evaluate(classifier, transform_text([' '.join(x) for x in X_data]), Y_data)

def process_text(text):
    ''' trains w2v model on given texts'''
    ''' list of strings, where string - full text'''
    text_list = [x.split(' ') for x in text]
    new_words = []
    for cur_text in text_list:
        ok = 1
        for word in cur_text:
            if word not in cur_model:
                ok = 0
        if not ok:
            new_words.append(cur_text)
    #print(new_words)
    #print(len(cur_model.wv.vocab))
    cur_model.build_vocab(new_words, update=True)
    cur_model.train(new_words, total_examples=len(new_words), epochs=10)
    #print(len(cur_model.wv.vocab))

def predict_text(text):
    '''string'''
    reforged_text = transform_text([text])
    print(reforged_text)
    result = classifier.predict(reforged_text)
    return result[0]
    '''0 or 1'''
"""



nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))
parsing = {}
m = Mystem()
tokenizer = RegexpTokenizer(r'[а-яА-Я]+')
window_length = 15		# размер окна
ad_coefficient = 0.7	# коэффициент рекламы


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
	clf -- работающая нейросеть.
	"""
	def  __init__(self):
		"""Конструктор."""
		self.vectorizer = CountVectorizer()


	"""Word to vector:"""
	def transform_text(self, data):
		''' list of strings '''
		result = []
		for text in data:
			now = [self.w2v_model.wv[token] for token in text.split(' ') if token in self.w2v_model.wv]
			if len(now) == 0:
				result.append(np.array([0] * 100))
			else:
				result.append(np.mean(now, axis=0))
		return result
		# return [np.mean([self.w2v_model.wv[token] for token in text.split(' ') if token in self.w2v_model.wv], axis=0) for text in data]


	def train_w2v(self, data):
		return word2vec.Word2Vec(data, workers=4, size=100, min_count=2, window=4, sample=1e-3)


	def predict_text(self, text):
		reforged_text = transform_text([text])
		print(reforged_text)
		result = classifier.predict(reforged_text)
		return result[0]
	"""End."""


	def load(self):
		"""Загрузка модели."""
		data = self.load_result()
		self.data = data
		x = data[0]
		y = data[1]
		# self.w2v_model = word2vec.Word2Vec(data[0], workers=4, size=100, min_count=2, window=4, sample=1e-3)
		# self.w2v_model = self.train_w2v(x)
		# xxx = self.transform_text([' '.join(xx) for xx in x])
		# print(type(xxx))
		# print(len(xxx))
		# print(type(xxx[0]))
		# self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(xxx, y, test_size=0.33, random_state=42)
		# print(type(self.x_train))
		# print(len(self.x_train))
		# for train in self.x_train:
		#	print(len(train))
		# print(type(self.y_train))
		# print(len(self.y_train))
		# print(type(self.y_train[0]))
		# self.clf_log = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(20, 2), random_state=100).fit(self.x_train, self.y_train)
		self.x_data = self.vectorizer.fit_transform(data[0])
		# self.x_data = self.normilize_data(data[0])
		self.y_data = data[1]
		self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x_data, self.y_data, test_size=0.33, random_state=42)
		start = time.time()
		self.clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(2, 2), random_state=100).fit(self.x_train, self.y_train)
		print('Time : ' + str(time.time() - start))


	def normilize_data(self, data):
		"""Нормализирует данные -> не используется."""
		w = self.vectorizer.fit_transform(data)
		new_count = []
		for i in range(len(data)):
			new_count.append(w[i] / len(data[i].split(' ')))
		return vstack(new_count)


	def load_result(self):
		""""Загрузка готовых данных."""
		files = glob.glob('./ans/*.txt')
		data = [[], []]
		for now in files:
			print('Load : ' + now)
			res = ParseTrain(now).parse_result()
			if res == None:
				continue
			data[0].append(res[0])
			data[1].append(res[1])
		print('Loaded ' + str(len(files)) + ' files')
		return self.large_window(data)


	def create_window(self, data):
		"""Создание окна фиксированной длины -> не используется."""
		ans = [[], []]
		for index in range(len(data[0])):
			x = data[0][index]
			y = data[1][index]
			for i in range(len(x) - window_length + 1):
				text = ''
				sum = 0
				for j in range(window_length):
					text += x[i + j] + ' '
					sum += y[i + j]
				ans[0].append(text)
				ans[1].append(1 * (sum / window_length >= 0.5))
		return ans


	def large_window(self, data):
		"""Создание окна на всём отрезке."""
		ans = [[], []]
		for index in range(len(data[0])):
			x = data[0][index]
			y = data[1][index]
			i = 0
			while i < len(y):
				start = i
				text = ''
				while i < len(y):
					if y[i] == y[start]:
						text += x[i] + ' '
						i += 1
					else:
						break
				ans[0].append(text)
				ans[1].append(y[start])
		return ans


	def large_window2(self, data):
		"""Создание окна на всём отрезке -> не используется."""
		x_data = data[0]
		y_data = data[1]
		l_now = 0
		r_now = 0
		for i in range(0, len(x_data)):
			sum = 0
			for j in range(i, len(y_data)):
				sum += y[j]
				if r_now - l_now < j - i + 1 and sum / (j - i + 1) >= ad_coefficient:
					l_now = i
					r_now = j
		return (l_now, r_now)


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
		print('Evaluation:')
		print('Accuracy : {:.3f}'.format(skm.accuracy_score(labels, predictions)))
		print('Precision : {:.3f}'.format(skm.precision_score(labels, predictions)))
		print('Recall : {:.3f}'.format(skm.recall_score(labels, predictions)))
		# print(self.data[0])
		# print(self.data[0][0])
		# predictions = self.transform_text([' '.join(x) for x in self.data[0]])
		# print(len(predictions[0]))
		# print(len(self.clf_log.coef_[0]))
		# predictions = self.clf_log.predict(predictions)
		# print('Evaluation2:')
		# print('Accuracy : {:.3f}'.format(skm.accuracy_score(self.data[1], predictions)))
		# print('Precision : {:.3f}'.format(skm.precision_score(self.data[1], predictions)))
		# print('Recall : {:.3f}'.format(skm.recall_score(self.data[1], predictions)))


	def predict(self, text):
		"""Предсказание по готовым данным."""
		text = self.vectorizer.transform([text])
		return self.clf.predict_proba(text)[0][1] >= ad_coefficient	# это реклама?


	def predict_with_parse(self, text):
		"""Предсказание по не обработанным данным."""
		text = self.preprocess_dataset(text)
		text = self.process_dataset([text])
		text = self.vectorizer.transform(text)
		return self.clf.predict_proba(text)[0][1]	# это реклама?
