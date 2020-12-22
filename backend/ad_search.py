import requests
import json
import xmltodict
from bs4 import BeautifulSoup
from neuro_search import NeuroSearch
from neuro_search import window_length
import glob
from parse_train import ParseTrain


youtubeUrl = 'https://www.youtube.com/watch?v='
timedtextVar = 'var ytInitialPlayerResponse = '
ads_list = ['подарок', 'чайник']
neuroSearch = NeuroSearch()
neuroSearch.load()
neuroSearch.evaluate()


class AdSearch:
	"""
	Класс ищет рекламу в субтитрах.

	Поля класса:
	videoUrl -- абсолютная ссылка на видео.
	timedtextUrl -- абсолютная ссылка на субтитры.
	timedtext -- субтитры в виде: [start, duration, text].
	ads -- список рекламы в виде: [start, duration, text].
	ads_json -- ads в виде JSON.

	Ошибки класса:
	ValueError('No input video') -- отсутсвует ссылка на видео.
	"""
	def  __init__(self, videoUrl):
		"""Создаёт объект для поиска рекламы по короткой ссылке видео."""
		if videoUrl is None:
			raise ValueError('No input video')
		self.videoUrl = youtubeUrl + videoUrl


	def find(self):
		"""Ищет рекламу на видео."""
		self.timedtextUrl = self.parse_html()
		self.timedtext = self.create_window(self.parse_xml())
		self.ads = self.get_ads()
		self.ads_json = self.ads_to_json()
		return self.ads_json


	def parse_html(self):
		"""Получает субтитры из html страницы."""
		r = requests.get(self.videoUrl)
		html_parser = BeautifulSoup(r.text, 'html.parser')
		scripts = html_parser.find_all('script')
		result = None
		for script in scripts:
			if script.string is not None and timedtextVar in script.string:
				result = script.string
		json_text = result.replace(timedtextVar, '').replace(';', '')
		data = json.loads(json_text)
		return data['captions']['playerCaptionsTracklistRenderer']['captionTracks'][0]['baseUrl']


	def parse_xml(self):
		"""Приводит субтитры в нужный вид."""
		r = requests.get(self.timedtextUrl)
		data = xmltodict.parse(r.text)
		data = json.loads(json.dumps(data))
		result = []
		for subtitle in data['transcript']['text']:
			result.append([ float(subtitle['@start']), float(subtitle['@dur']), subtitle['#text'] ])
		return result


	def create_window(self, subtitles):
		"""Создает окно."""
		result = []
		for i in range(len(subtitles) - window_length + 1):
			start = subtitles[i][0]
			finish = subtitles[i + window_length - 1][0] + subtitles[i + window_length - 1][1]
			text = ''
			for j in range(window_length):
				text += subtitles[i + j][2] + ' '
			result.append([start, finish - start, text])
		return result


	def get_ads(self):
		"""Получает рекламу из субтитров."""
		result = []
		ans = []
		last = False
		subtitles = [neuroSearch.preprocess_dataset(subtitle[2]) for subtitle in self.timedtext]
		subtitles = neuroSearch.process_dataset(subtitles)
		for index in range(len(self.timedtext)):
			subtitle = self.timedtext[index]
			if self.check_subtitle(subtitles[index]):
				if last:
					start = min(result[-1][0], subtitle[0])
					finish = max(result[-1][0] + result[-1][1], subtitle[0] + subtitle[1])
					result[-1] = [start, finish - start]
				else:
					 result.append([subtitle[0], subtitle[1]])
					 last = True
			else:
				last = False
		i = 0
		while i < len(result):
			l_now = result[i][0]
			r_now = result[i][1]
			for j in range(i, len(ans)):
				l_video = result[j][0]
				r_video = result[j][1]
				if l_now <= l_video and l_video <= r_now:
					r_now = r_video
					i = j
				else:
					break
			ans.append([l_now, r_now])
			i += 1
		return ans


	def check_subtitle(self, text):
		"""Проверяет один субтитр на рекламу."""
		return neuroSearch.predict(text)


	def ads_to_json(self):
		"""Преобразует внутреннее представление в JSON."""
		result = {'subtitles' : []}
		for subtitle in self.ads:
			result['subtitles'].append({'start' : subtitle[0], 'dur' : subtitle[1]})
		return result


	def evaluate_ranges(self):
		"""Качество модели для всех файлов."""
		files = glob.glob('./res/*.xml')
		for file in files[0:1]:
			train = ParseTrain(file)
			ans_true = train.parse_ranges()
			search = AdSearch(train.get_video_url())
			search.find()
			ans_our = search.ads
			self.evaluate_answers(ans_our, ans_true)


	def evaluate_answers(self, ans_our, ans_true):
		"""Качество модели для одного файла."""
		print('True answer : ' + str(ans_true))
		print('Our answer : ' + str(ans_our))
		intersection = 0
		len_true = 0
		len_our = 0
		len_intersection = 0
		l_true = 0
		r_true = 0
		for i in range(len(ans_true)):
			len_true += ans_true[i][1]
		for i in range(len(ans_our)):
			len_our += ans_our[i][1]
		for i in range(len(ans_true)):
			l_true = ans_true[i][0]
			r_true = l_true + ans_true[i][1]
		for j in range(len(ans_our)):
			l_now = ans_our[j][0]
			r_now  = l_now + ans_our[j][1]
			if (l_now <= l_true and l_true <= r_now):
				len_intersection += min(r_now, r_true) - l_true
			elif (l_now <= r_true and r_true <= r_now):
				len_intersection += r_true - l_now
			elif (l_true <= l_now and r_now <= r_true):
				len_intersection += r_now - l_now
		intersection = 1
		accuracy = 1
		if len_true:
			intersection = len_intersection / len_true
		if len_our:
			accuracy = len_true / len_our
		res = [accuracy, intersection, 2 * accuracy * intersection / (accuracy + intersection)]
		print('Result : ' + str(res))
		return res
