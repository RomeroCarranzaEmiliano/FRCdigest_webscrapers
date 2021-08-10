"""
	setup.py
"""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
	README = readme_file.read()

with open('HISTORY.md') as history_file:
	HISTORY = history_file.read()

setup_args = dict(
	name='FRCdigest_webscrapers',
	version='0.1',
	description='Webscrapers for the FRCdigest discord bot',
	long_description_content_type='text/markdown',
	long_description=README + '\n\n' + HISTORY,
	license='',
	packages=find_packages(),
	author='Emiliano Romero Carranza',
	author_email='romerocarranzaemiliano@gmail.com',
	keywords=['FRCdigest', 'webscraper', 'discord', 'bot'],
	url='https://github.com/RomeroCarranzaEmiliano/FRCdigest_webscrapers',
	download_url=''
)

install_requires = [
	
]

if __name__ == '__main__':
	setup(**setup_args, install_requires=install_requires)