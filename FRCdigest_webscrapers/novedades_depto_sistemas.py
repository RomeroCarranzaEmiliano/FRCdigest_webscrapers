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
		title = panel.find(class_="panel-heading titulo-noticia").find("a").get_text()

		content = panel.find(class_=\
			"panel-body content-scroll descripcion-noticia ps-container").find("div")\
			.get_text()

		images = []
		for img in panel.find(class_=\
			"panel-body content-scroll descripcion-noticia ps-container").find_all("img"):
			img_url = "https://www.institucional.frc.utn.edu.ar"+img["src"]
			images.append(img_url)

		link = title = panel.find(class_=\
			"panel-heading titulo-noticia").find("a")["href"]
		link = "https://www.institucional.frc.utn.edu.ar"+link

		news.append({
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
	stored_stack = []

	if os.path.exists(filename):
		if os.path.getsize(filename):
			file = open(filename, "rb")
			stored_stack = pickle.load(file)
			file.close()
		
	# Open if exists, or create the file
	file = open(filename, "wb")

	if stored_stack != []:
		# There is a stored stack, so a comparation must be done
		# News found in the stored_stack will be removed from the news vector
		for i in range(len(stack)):
			if stack[i] == stored_stack[i]:
				news.pop(i)

	if len(news) > 0:
		# Save new news
		# Point to the start of the file
		file.seek(0)

		# Write
		pickle.dump(news, file)

		# Delete old data
		file.truncate()
		file.close()

		return news
	else:
		file.close()

		return False


if __name__ == "__main__":
	pass


""" NOTES
	-----


"""