import requests
import json
import xmltodict
from bs4 import BeautifulSoup


youtubeUrl = 'https://www.youtube.com/watch?v='
timedtextVar = 'var ytInitialPlayerResponse = '


class AdSearch:
	"""
	Класс ищет рекламу в субтитрах.
	
	Поля класса:
	videoUrl -- абсолютная ссылка на видео.
	timedtextUrl -- абсолютная ссылка на субтитры.
	timedtext -- субтитры в виде: [start, duration, text].
	
	Ошибки класса:
	ValueError('No input video') -- отсутсвует ссылка на видео.
	"""
	def  __init__(self, videoUrl):
		"""Создаёт объект для поиска рекламы по короткой ссылке видео."""
		if videoUrl is None:
			raise ValueError('No input video')
		self.videoUrl = youtubeUrl+ videoUrl
	
	
	def find(self):
		"""Ищет рекламу на видео."""
		self.timedtextUrl = self.parse_html()
		self.timedtext = self.parse_xml()
		return str(self.timedtext)
	
	
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
			result.append([ subtitle['@start'], subtitle['@dur'], subtitle['#text'] ])
		return result

