import xmltodict


class ParseTrain:
	"""
	Класс парсит обучающую выборку
	
	Поля класса:
	file_name -- имя файла.
	"""
	def  __init__(self, file_name):
		self.file_name = file_name
	
	
	def parse(self):
		with open(self.file_name, 'r', encoding='UTF-8') as f:
			data = f.read()
		data = xmltodict.parse(data)
		result = [[], []]
		ad_count = 0
		for subtitle in data['data']['subtitles']['part']:
			if '@ad' in subtitle.keys():
				if subtitle['@ad'] == 'start':
					ad_count += 1
				else:
					ad_count -= 1
			if '#text' in subtitle.keys():
				result[0].append(subtitle['#text'])
			else:
				continue
			if ad_count > 0:
				result[1].append(1)
			else:
				result[1].append(0)
		return result

