#!/usr/bin/python

import re
import xml.etree.cElementTree as ET
import xml.dom.minidom
import json

DATA = 'dictionary.txt'
XML = 'dictionary.xml'
JSON = 'dictionary.json'
DICTIONARY = []

def parse(filename):
	f = open(filename, 'r')
	d = f.read().splitlines()

	WORD = {}
	define = False
	etymology = False

	for line in d[29:]:
		if((len(line.split(" ")) == 1) and (re.search(r'^[A-Z]+$', line))):
			define = False
			DICTIONARY[len(DICTIONARY):] = [WORD]
			WORD = {'word':'', 'defn':'', 'etym':''}
			WORD['word'] = line
			continue
		if(re.search(r'.*Defn:.*', line) and not define):
			WORD['defn'] = line.decode('ascii', 'ignore')
			define = True
			continue
		if(re.search(r'.*Etym.*', line)):
			WORD['etym'] = line.decode('ascii', 'ignore')
			etymology = True
			continue
		if((line != "") and etymology):
			WORD['etym'] = WORD['etym'] + line.decode('ascii', 'ignore')
			continue
		if((line == "")):
			etymology = False
			define = True
			continue
		elif(define):
			WORD['defn'] = WORD['defn'] + line.decode('ascii', 'ignore')
			continue

def generateXML(filename):
	dictionary = ET.Element("dictionary")

	for w in DICTIONARY[1:]:
		word = ET.SubElement(dictionary, "word", name=w['word'])
		defn = ET.SubElement(word, "defn")

		if(w['defn']):
			defn.text = w['defn']
		
		etym = ET.SubElement(word, "etym")
		if(w['etym']):
			etym.text = w['etym']

	data = ET.ElementTree(dictionary)
	data.write(filename)

	dom = xml.dom.minidom.parse(filename)

	f = open(filename, 'w')
	f.write(dom.toprettyxml())
	f.close()

def generateJSON(filename):
	dictionary = {}

	for w in DICTIONARY[1:]:
		word = w['word']
		dictionary[word] = {"defn": w['defn'], "etym": w['etym']}

	data = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))

	f = open(filename, 'w')
	f.write(data)
	f.close()

if __name__ == '__main__':
	parse(DATA)
	generateXML(XML)
	generateJSON(JSON)