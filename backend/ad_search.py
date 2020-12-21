import requests
import json
import xmltodict
from bs4 import BeautifulSoup
from neuro_search import NeuroSearch


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
		self.timedtext = self.parse_xml()
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
	
	
	def get_ads(self):
		"""Получает рекламу из субтитров."""
		result = []
		last = False
		for subtitle in self.timedtext:		# окно
			if self.check_subtitle(subtitle[2]):
				if last:
					start = min(result[-1][0], subtitle[0])
					finish = max(result[-1][0] + result[-1][1], subtitle[0] + subtitle[1])
					result[-1] = [start, finish - start]
				else:
					 result.append([subtitle[0], subtitle[1]])
					 last = True
			else:
				last = False
		return result
	
	
	def check_subtitle(self, text):	# окно
		"""Проверяет один субтитр на рекламу."""
		for ad_word in ads_list:
			if ad_word in text:
				return True
		return False
	
	
	def ads_to_json(self):
		"""Преобразует внутреннее представление в JSON."""
		result = {'subtitles' : []}
		for subtitle in self.ads:
			result['subtitles'].append({'start' : subtitle[0], 'dur' : subtitle[1]})
		return result
