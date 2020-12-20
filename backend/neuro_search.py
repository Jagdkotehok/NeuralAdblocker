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


nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))
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
		self.vectorizer = CountVectorizer()
	
	
	def load(self):
		data = self.get_data_for_load() # data[0] -> test, data[1] -> answer
		# print(data)
		# print(type(self.vectorizer))
		# self.x_data = self.vectorizer.fit_transform(data[0])
		# self.y_data = data[1]
		# self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x_data, self.y_data, test_size=0.33, random_state=42)
		# self.clf = LogisticRegression(random_state=42, max_iter=1000).fit(self.x_train, self.y_train)
	
	
	def get_data_for_load(self):
		files = glob.glob('./res/*.xml')
		result1 = []
		result2 = []
		for now in files[0:1:]:
			print("Parse : " + now)
			data = ParseTrain(now).parse()
			# print(data)
			for index in range(len(data[0])):
				print(self.preprocess_data(data[0][index]))
		print('Files : ' + str(len(files)))
		print(result1)
		print(result2)
		result = '123 ЕНПФ пакета облигаций ТОО "Бузгул Аурум" было начато по инициативе Национального банка'
		result = self.preprocess_data(result)
		print(result)
		result2 = [0 for _ in range(5)]
		result2 += [1 for _ in range(5)]
		return [result, result2]
	
	
	def preprocess_data(self, data):
		tokens = [token for token in tokenizer.tokenize(data.lower()) if token not in stop_words]
		tokens = [m.lemmatize(token)[0] for token in tokens]
		return tokens
	
	
	def evaluate(self):
		predictions = self.clf.predict(self.x_test)
		labels = self.y_test
		print("Accuracy {:.3f}".format(skm.accuracy_score(labels, predictions)))
		print("Precision {:.3f}".format(skm.precision_score(labels, predictions)))
		print("Recall {:.3f}".format(skm.recall_score(labels, predictions)))
