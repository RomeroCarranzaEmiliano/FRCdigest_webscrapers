"""
	api.py

	Api para acceder a los webscrapers desde el bot
"""


import discord
from . import novedades_depto_sistemas


def news_systems_department():
	"""
		Call the scraper, get the news
	"""
	# Get the news
	news = novedades_depto_sistemas.scrap()


	# Return de discord messages
	return news

