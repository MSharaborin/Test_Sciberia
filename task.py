import os
import pickle
from datetime import datetime

import imageio
import natsort
import numpy as np
from PIL import Image



PATH_DIR = 'all files/'
FPS = 10


def check_dir(workDir):
	"""
	Проверяем количество серий снимков в рабочей папке
	"""
	try:
		return os.listdir(workDir)
	except FileNotFoundError:
		return 'The specified directory was not found'


def create_dict(workDir=list):
	"""
	Создаем словарь с директориями серий снимков для обработки
	"""
	dictionaryWithSnapshots = {}
	for dir in workDir:
		dictionaryWithSnapshots[dir] = ''
	return dictionaryWithSnapshots


def fill_in_data(dictionaryWithSnapshots, flag = None):
	"""
	Заполняем снимками словарь
	"""
	for dirName, listSnapshots in dictionaryWithSnapshots.items():
		listSnapshots = []
		try:
			for file in natsort.natsorted(os.listdir(PATH_DIR + str(dirName))):
				print(file)
				with open(PATH_DIR + str(dirName) + '/' + file, 'rb') as f:
					try:
						dataNdarray = pickle.load(f)
						# перевод в RGB
						imageUint8 = Image.fromarray(dataNdarray)
						imageRBG = imageUint8.convert("RGB")
						rgbArray = np.array(imageRBG)
						# перевод в RGB-grayscale-изображение (градации серого от 0 до 255)
						imageRBGgrayscale = (rgbArray * 255).astype('uint8')
						rgbGrayscaleArray = np.array(imageRBGgrayscale)

						if flag == 'RGB':
							listSnapshots.append(rgbArray)
						elif flag == 'RGB-grayscale':
							listSnapshots.append(rgbGrayscaleArray)
						else:
							listSnapshots.append((dataNdarray))
					except EOFError:
						continue
		except FileNotFoundError:
			return 'The specified directory was not found'
		except NotADirectoryError:
			return f'Invalid folder name: {PATH_DIR + str(dirName)}'
		dictionaryWithSnapshots[dirName] = np.array(listSnapshots)
	return dictionaryWithSnapshots


def create_gif_animation(dictionaryWithSnapshots, name = ''):
	"""
	Создаем gif анимацию из серий снимков
	"""
	try:
		for dirName, listSnapshots in dictionaryWithSnapshots.items():
			start = datetime.now()
			imageio.mimwrite(name + ' ' + str(dirName) + '.gif', listSnapshots,  format = None,  fps=FPS)
			total = datetime.now() - start
			print(f'Время обработки: {name} {dirName} - {total}')
	except AttributeError:
		return 'Error: the folder may not be specified correctly or the files may not meet the requirements'
	except RuntimeError:
		return 'The folder is empty'


if __name__ == '__main__':    
	start = datetime.now()
	print('1) Серии снимков')
	print(create_gif_animation(fill_in_data(create_dict(workDir=check_dir(PATH_DIR)))))
	print('2) Серии снимков RBG')
	print(create_gif_animation(fill_in_data(create_dict(workDir=check_dir(PATH_DIR)), 'RGB'), 'RGB'))
	print('3) Серии снимков RGB-grayscale')
	print(create_gif_animation(fill_in_data(create_dict(workDir=check_dir(PATH_DIR)), 'RGB-grayscale'),'RGB-grayscale'))
	total = datetime.now() - start
	print(f'Время работы скрипта : {total}')
