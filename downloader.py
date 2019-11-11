#Adi has made this just a *little* challenging. Website looks great, but I would hardly describe it as "bot-accessible."
#That's really the goal of my work, is to make this programmatically accessible without creating massive amounts of requests to his website.
#I am deeply thankful to Adi for releasing his work under Creative Commons 4.0.

#I have published this script so that you can understand how I got the data. Please do not abuse his website. There is a full copy of the database available in the same repo.
from lxml import html
import lxml.etree as ET
import requests
import sys
import time
import math
from matplotlib import collections as mc
import matplotlib.pyplot as plt
import numpy as np
import bezier
import re
from svgpathtools.parser import parse_path
import json

def main():
	#Let's start with a little request to his main page:
	homepage = html.fromstring(requests.get("https://thedoodlelibrary.com").text)
	categorynames = homepage.xpath('./body/div[@class="w-container"]/div/div[@class="h4"]/@id')
	categorylinks = homepage.xpath('./body/div[@class="w-container"]/div/div[@class="alldiv"]/a/@href')
	categories = {categorynames[i]:categorylinks[i] for i in range(len(categorynames))}

	alldoodlesraw = {}
	totaldoodles = 0

	#This could be a dict comprehension, but, come on, there's a limit... Readability is important too
	for category in categories:
		categorysample = html.fromstring(requests.get(categories[category]).text)
		alldoodlesraw[category] = categorysample.xpath('./body/div/div/div[contains(@class, "collection-list")]/div/a/@href')
		totaldoodles += len(alldoodlesraw[category])
	
	catdb = {}
	doodledb = {}

	plt.ion()
	n = 0
	for cat in alldoodlesraw:
		for doodleraw in alldoodlesraw[cat]:
			try:
				progbar(n/totaldoodles, 100)
				n += 1
				name, doodle = scrapeDoodle(doodleraw)
				if (cat not in catdb):
					catdb[cat] = []
				
				catdb[cat].append(name)
				doodledb[name] = doodle
				plt.close()
				debugDoodle(doodle)
				plt.pause(0.25)
				with open("doodledb.json", "w") as f:
					json.dump(doodledb, f)
			except:
				e = sys.exc_info()[0]
				print(e)
	
	with open("doodledb.json", "w") as f:
		json.dump({'categories':catdb, 'doodles':doodledb}, f)
	
	
	
	#/g/g[@id!="logo-footer"]/path/@d
def scrapeDoodle(url):
	print(url)
	doodlepage = html.fromstring(requests.get('https://www.thedoodlelibrary.com' + url).text)
	name = doodlepage.xpath('./body/div/div/div/div[@class="image-name"]/text()')[0]
	print(name)
	resource = doodlepage.xpath('./body/div/div/div/a[contains(@class, "download")]/@href')[0]
	svg = ET.XML(requests.get(resource).content)
	paths = svg.xpath('svg:g/svg:g[@id!="logo-footer"]/svg:path/@d', namespaces={'svg': 'http://www.w3.org/2000/svg'}) + svg.xpath('svg:g/svg:path/@d', namespaces={'svg': 'http://www.w3.org/2000/svg'})#In general, this will select both the gray transparent stuff, and the black lines. For my purposes, that's fine.
	strokes = []
	for path in paths:
		strokes += extractStrokes(path)
	return name,strokes
	

def debugDoodle(strokes):
	lc = mc.LineCollection(strokes, linewidths=2)
	fig, ax = plt.subplots()
	ax.add_collection(lc)
	ax.autoscale()
	ax.margins(0.1)
	plt.show()

def extractStrokes(path):
	bezpath = parse_path(path)
	n = 100
	ptpath = [bezpath.point(t) for t in np.linspace(0, 1, n)]
	return [((ptpath[i%n].real, ptpath[i%n].imag), (ptpath[(i+1)%n].real, ptpath[(i+1)%n].imag)) for i in range(n)]
	
def progbar(p, n=20):
	i = math.floor(p*n)
	sys.stdout.write(("[%-"+str(n)+"s] %d%%") % ('='*i, math.floor(p * 100)))
	sys.stdout.write('\r')
	sys.stdout.flush()



main()

#debugDoodle(scrapeDoodle('/drawings/reading')[1])
