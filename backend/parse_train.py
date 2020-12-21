import xmltodict


class ParseTrain:
	"""
	Класс парсит обучающую выборку
	
	Поля класса:
	file_name -- имя файла.
	"""
	def  __init__(self, file_name):
		"""Сохраняет имя файла."""
		self.file_name = file_name
	
	
	def parse_data_set(self):
		"""Загрузка не готовых данных."""
		with open(self.file_name, 'r', encoding='UTF-8') as f:
			data = f.read()
		data = xmltodict.parse(data)
		result = [[], []]
		ad_count = 0
		for subtitle in data['data']['subtitles']['part']:
			if '@ad' in subtitle.keys() and subtitle['@ad'] == 'start':
				ad_count += 1
			if '#text' in subtitle.keys():
				result[0].append(subtitle['#text'])
			else:
				if '@ad' in subtitle.keys() and subtitle['@ad'] == 'end':
					ad_count -= 1
				continue
			if ad_count > 0:
				result[1].append(1)
			else:
				result[1].append(0)
			if '@ad' in subtitle.keys() and subtitle['@ad'] == 'end':
				ad_count -= 1
		return result
	
	
	def parse_result(self):
		"""Загрузка готового результата."""
		name = self.file_name
		index = name[-5]
		if index == '2':
			return None
		with open(name, 'r', encoding='UTF-8') as f:
			array1 = f.read()[2:-2].split("', '")
		name = name[:-5] + '2.txt'
		with open(name, 'r', encoding='UTF-8') as f:
			array2 = f.read()[1:-1].split(', ')
		array2 = [int(_) for _ in array2]
		return [array1, array2]

