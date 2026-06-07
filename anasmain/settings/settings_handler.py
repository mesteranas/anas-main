from configparser import ConfigParser
import locale
import os,shutil
from . import app
appName=app.appName
cpath=os.path.join(os.getenv('appdata'),appName,"settings.ini")
if not os.path.exists(os.path.join(os.getenv('appdata'),appName)):
	os.mkdir(os.path.join(os.getenv('appdata'),appName))
def getSystemLanguage():
	try:
		systemlanguage, encoding = locale.getdefaultlocale()
		languages=os.listdir("data/languages")
		for language in languages:
			if language.lower() in systemlanguage.lower():
				return language
		return "en"
	except:
		return "en"
settingsConfig={
	"g":{
		"lang":getSystemLanguage(),
		"exitdialog":"True",
	},
	"update":{
		"autoCheck":"True",
		"beta":"False"
	}
}
if not os.path.exists(cpath):
	config = ConfigParser() 
	for section,values in settingsConfig.items():
		config.add_section(section)
		for key,value in values.items():
			config[section][key]=value
	with open(cpath, "w",encoding="utf-8") as file:
		config.write(file)

def get(section,key):
	try:
		config = ConfigParser()
		config.read(cpath)
		value = config[section][key]
		return value
	except:
		try:
			return settingsConfig[section][key]
		except:
			return ""

def set(section,key, value):
		config = ConfigParser()
		config.read(cpath)
		try:
			config[section][key] = value
		except KeyError:
			config.add_section(section)
			config[section][key] = value
		with open(cpath, "w",encoding="utf-8") as file:
			config.write(file)