"""
	novedades_depto_sistemas.py

	Webscraper para obtener las últimas novedades en la página del departamento de sistemas de la 
	UTN FRC

"""


import dryscrape
import sys
import time
from bs4 import BeautifulSoup
import re
import pickle
import os


def scrap():
	"""
		Scrap the website

		Scrap and get an array of news from the page
	"""

	if "linux" in sys.platform:
		# Start xvfb in case no other X is running
		dryscrape.start_xvfb()

	search_term = "dryscrape"

	url = "https://www.institucional.frc.utn.edu.ar/sistemas/Areas/Institucional/Novedades.asp"

	# Set up a web scraping session
	sess = dryscrape.Session(base_url = url)

	# Don't neeed images
	sess.set_attribute("auto_load_images", False)

	sess.visit(url)

	time.sleep(2.5)

	html = sess.body()

	soup = BeautifulSoup(html, 'html.parser')

	panels = soup.find_all(class_="panel panel-default")

	news = []
	for panel in panels:
		# Get all the needed data
		title = panel.find(class_="panel-heading titulo-noticia").find(class_="link_noticia").get_text()

		content = panel.find(class_=\
			"panel-body content-scroll descripcion-noticia ps-container").find("div")\
			.get_text()

		images = []
		for img in panel.find(class_=\
			"panel-body content-scroll descripcion-noticia ps-container").find_all("img"):
			img_url = "https://www.institucional.frc.utn.edu.ar"+img["src"]
			images.append(img_url)

		link = panel.find(class_=\
			"panel-heading titulo-noticia").find("a")["href"]
		link = "https://www.institucional.frc.utn.edu.ar"+link

		# Ignore everything that is not after the last '/' of the link
		code = link.split("/")
		code = code[-1]
		# Grab everything after '?'
		code = code.split("?")
		code = code[-1]

		news.append({
			"code": code,
			"title": title,
			"content": content,
			"images": images,
			"link": link
			})

	"""
		Compare data and detect if there is a new post. Grab the new posts.
	"""

	filename = "stack.data"

	# Create stack
	stack = []
	for a in news:
		stack.append(a["code"])

	stored_stack = []

	if os.path.exists(filename):
		if os.path.getsize(filename):
			file = open(filename, "rb")
			stored_stack = pickle.load(file)
			file.close()
		

	# Open if exists, or create the file
	file = open(filename, "wb")

	trimed_news = []
	for j in range(len(news)):
		if not(news[j]["code"] in stored_stack):
			trimed_news.append(news[j])


	file.seek(0)
	pickle.dump(stack, file)
	file.truncate()
	file.close()

	if trimed_news != []:
		return trimed_news
	else:
		return False


if __name__ == "__main__":
	pass


""" NOTES
	-----


"""