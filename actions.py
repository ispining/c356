from pyautogui import moveTo, click, rightClick, doubleClick, dragTo, write
from keyboard import press_and_release
import time, os, subprocess, threading
import psycopg as db_connect



def db_connector():
	try:
		db = db_connect.connect(
		dbname="client356",
		user="postgres",
		password="armageddon",
		host="illyashost.ddns.net",
		port=5432)
		sql = db.cursor()
		return db, sql
	except db_connect.OperationalError:
		return db_connector()

def settings(setting, new_val=None):
	db, sql = db_connector()
	sql.execute(f"SELECT * FROM settings WHERE setting = '{str(setting)}'")
	if sql.fetchone() is None:
		sql.execute(f"INSERT INTO settings VALUES ('{str(setting)}', 'None')")
		db.commit()
	if new_val != None:
		sql.execute(f"UPDATE settings SET value = '{str(new_val)}' WHERE setting = '{str(setting)}'")
		db.commit()
	else:
		sql.execute(f"SELECT * FROM settings WHERE setting = '{str(setting)}'")
		return sql.fetchall()[0][1]

def urlClick():
	moveTo(700, 120, 0.1)
	click()


def urlContinueClick():
	moveTo(767, 121)
	click()

def continueToChatButtonClick():
	moveTo(456, 542, 0.1)
	click()

	moveTo(476, 542, 0.1)
	click()

def useWebAppLinkClick():
	moveTo(477, 445, 0.1)
	click()

def chatTextAreaPaste():
	moveTo(635, 1113, 1)
	rightClick()
	time.sleep(1)
	moveTo(720, 909, 1)
	click()

def sendMsgButtonClick():
	moveTo(911, 1104, 0.1)
	click()

def emulateKey(copy=False, paste=False, selectAll=False, enter=False):
	if copy:
		press_and_release("Ctrl+c")
	elif paste:
		press_and_release("Ctrl+v")
	elif selectAll:
		press_and_release("Ctrl+a")
	elif enter:
		press_and_release("enter")

def insertUrl(url: str):
	write(url, 0.1)

def parseContentFromDbToFile():
	def db_connector():
		try:
			db = db_connect.connect(
			dbname="client356",
			user="postgres",
			password="armageddon",
			host="illyashost.ddns.net",
			port=5432)
			sql = db.cursor()
			return db, sql
		except db_connect.OperationalError:
			return db_connector()
	db, sql = db_connector()
	try:
		sql.execute(f"SELECT * FROM settings WHERE setting = 'content'")
		content = sql.fetchall()[0][1]
		with open("/root/Desktop/WApp/content", "w") as file:
			file.write(content)
		return "/root/Desktop/WApp/content"

	except db_connect.OperationalError:
		parseContentFromDbToFile()

def parseNotifContentFromDbToFile(medormas):
	def db_connector():
		try:
			db = db_connect.connect(
			dbname="client356",
			user="postgres",
			password="armageddon",
			host="illyashost.ddns.net",
			port=5432)
			sql = db.cursor()
			return db, sql
		except db_connect.OperationalError:
			return db_connector()
	db, sql = db_connector()
	try:
		sql.execute(f"SELECT * FROM settings WHERE setting = '{medormas}_notif'")
		content = sql.fetchall()[0][1]
		with open("/root/Desktop/WApp/content", "w") as file:
			file.write(content)
		return "/root/Desktop/WApp/content"

	except db_connect.OperationalError:
		parseNotifContentFromDbToFile()

def copyContentFromFile():
	def openMousePad():
		subprocess.call("""mousepad /root/Desktop/WApp/content""", shell=True)
	threading.Thread(target=openMousePad, daemon=True).start()
	threading.main_thread()

	time.sleep(5)
	moveTo(57, 66, 0.5)
	click()
	time.sleep(0.1)
	moveTo(143, 264, 0.5)
	click()
	time.sleep(1)
	moveTo(57, 66, 0.5)
	click()
	time.sleep(2)
	moveTo(87, 155, 0.5)
	click()
	time.sleep(1)
	moveTo(1912, 30, 0.5)
	click()

def sendMessage(phone):

	urlClick()
	insertUrl(f"wa.me/972{str(phone)}")
	urlContinueClick()
	time.sleep(5)
	continueToChatButtonClick()
	time.sleep(2)
	useWebAppLinkClick()
	time.sleep(50)

	parseContentFromDbToFile()
	copyContentFromFile()
	time.sleep(2)
	chatTextAreaPaste()
	time.sleep(2)
	sendMsgButtonClick()
	time.sleep(1)


# parseContentFromDbToFile()
# copyContentFromFile()