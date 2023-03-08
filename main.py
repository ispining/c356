import pyautogui
import threading
import datetime as dt
import subprocess, os
from actions import *
import datetime


def clear_console() -> None:
	subprocess.call(f"clear", shell=True)
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

#db, sql = db_connector()

def preDB():
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
		user_id TEXT PRIMARY KEY,
		first_name TEXT,
		last_name TEXT,
		tz TEXT,
		birth_date TEXT,
		known_from TEXT,
		comment TEXT,
		country TEXT,
		city TEXT,
		address TEXT,
		phone TEXT)""")
	db.commit()
	sql.execute("""CREATE TABLE IF NOT EXISTS callbacks (
		from_user TEXT PRIMARY KEY,
		to_user TEXT,
		callback_data TEXT

		)""")
	db.commit()
	sql.execute("""CREATE TABLE IF NOT EXISTS settings (
		setting TEXT PRIMARY KEY,
		value TEXT
		)""")
	db.commit()

def run(target: str, func_list: list) -> None:
	print(f"########## {target.upper()} ##########")
	print()

	for action in func_list:
		print("[+] Start function => " + action.__name__)
		try:
			r = action()
			if action.__name__ == "db_connector":
				global db
				global sql
				db, sql = r
				print("[+] Database inited")
			print(f"[+] Finished function => {action.__name__}")
		except Exception as ex:
			print(ex)
			print(f"[-] Error! Can't finish function => {action.__name__}")

		print()
	print()

run("start and init", [db_connector, preDB])

class User:
	def __init__(self):
		self.user_id = None
		self.first_name = None
		self.last_name = None
		self.tz = None
		self.birth_date = None
		self.known_from = None
		self.comment = None
		self.country = None
		self.city = None
		self.address = None
		self.phone = None

	def exists(self):
		if self.user_id != None:
			sql.execute(f"SELECT * FROM users WHERE user_id = '{str(self.user_id)}'")
		elif self.phone != None:
			sql.execute(f"SELECT * FROM users WHERE phone = '{str(self.phone)}'")

		if sql.fetchone() is None:
			return False
		else:
			return True

	def get(self):
		result = []
		if self.exists():
			if self.user_id != None:
				sql.execute(f"SELECT * FROM users WHERE user_id = '{str(self.user_id)}'")
			elif self.phone != None:
				sql.execute(f"SELECT * FROM users WHERE phone = '{str(self.phone)}'")
			elif self.phone == None and self.user_id == None:
				sql.execute(f"SELECT * FROM users")
			for i in sql.fetchall():
				result.append({
					"user_id": i[0],
					"first_name": i[1],
					"last_name": i[2],
					"tz": i[3],
					"birth_date": i[4],
					"known_from": i[5],
					"comment": i[6],
					"country": i[7],
					"city": i[8],
					"address": i[9],
					"phone": i[10]
					})
		return result

	def add(self):
		if not self.exists():
			if self.phone != None:
				if self.user_id == None:
					self.user_id = str(random.randint(11111111, 99999999))
				sql.execute(f"""INSERT INTO users VALUES(
				'{str(self.user_id)}',
				'{str(self.first_name)}',
				'{str(self.last_name)}',
				'{str(self.tz)}',
				'{str(self.birth_date)}',
				'{str(self.known_from)}',
				'{str(self.comment)}',
				'{str(self.country)}',
				'{str(self.city)}',
				'{str(self.address)}',
				'{str(self.phone)}')""")
				db.commit()

	def set(self, column, value):
		if self.user_id != None:
			sql.execute(f"UPDATE users SET {str(column)} = '{str(value)}' WHERE user_id = '{str(self.user_id)}'")
			db.commit()
		elif self.phone != None:
			sql.execute(f"UPDATE users SET {str(column)} = '{str(value)}' WHERE phone = '{str(self.phone)}'")
			db.commit()

def settings(setting, new_val=None):
	sql.execute(f"SELECT * FROM settings WHERE setting = '{str(setting)}")
	if sql.fetchone() is None:
		sql.execute(f"INSERT INTO settings VALUES ('{str(setting)}', 'None')")
		db.commit()
	if new_val != None:
		sql.execute(f"UPDATE settings SET value = '{str(new_val)}' WHERE setting = '{str(setting)}'")
		db.commit()
	else:
		sql.execute(f"SELECT * FROM settings WHERE setting = '{str(setting)}'")
		return sql.fetchall()[0][1]

class Callback:
	def __init__(self, user_id):
		self.user_id = user_id

	def exists(self):
		sql.execute(f"SELECT * FROM callbacks WHERE from_user = '{str(self.user_id)}'")
		if sql.fetchone() is None:
			return False
		else:
			return True

	def get(self):
		if not self.exists():
			sql.execute(f"INSERT INTO callbacks VALUES ('{str(self.user_id)}', '0000, 'None')")
			db.commit()
			sql.execute(f"INSERT INTO callbacks VALUES ('{str(0000)}', '{str(self.user_id)}, 'None')")
			db.commit()
		sql.execute(f"SELECT * FROM callbacks WHERE from_user = '{str(self.user_id)}'")
		for row in sql.fetchall():
			if row[2] == "None":
				sql.execute(f"UPDATE callbacks SET callback_data = 'None' WHERE from_user = '{str(self.user_id)}'")
				db.commit()
				return row[2]

	def send(self, callback):
		sql.execute(f"UPDATE callbacks SET callback_data = '{str(callback)}' WHERE to_user = '{str(self.user_id)}'")
		db.commit()

try:
	db.close()
except:
	pass



def check_notice(db, sql):
	sql.execute(f"""CREATE TABLE IF NOT EXISTS notifier(
	row_id TEXT PRIMARY KEY,
	phone TEXT,
	tattoo_date TEXT,
	notif_medic_every_hours TEXT,
	notif_master_every_days TEXT,
	last_notif_medic TEXT,
	last_notif_master TEXT,
	status TEXT
		)""")

	db.commit()
	sql.execute(f"SELECT * FROM notifier")
	for notif in sql.fetchall():
		phone = notif[1]
		if phone[0] == "0":
			phone = phone[1:]
		elif phone[:3] == "972":
			phone = phone[3:]

		last_time_medic = notif[5]
		if last_time_medic not in [None, "None"]:
			last_time_medic = datetime.datetime.strptime(last_time_medic, '%Y-%m-%d %H:%M:%S.%f')
			if last_time_medic + datetime.timedelta(hours=int(notif[3])) < datetime.datetime.now():
				urlClick()
				insertUrl(f"wa.me/972{str(phone)}")
				urlContinueClick()
				time.sleep(5)
				continueToChatButtonClick()
				time.sleep(4)
				useWebAppLinkClick()
				time.sleep(60)
				parseNotifContentFromDbToFile("medical")
				copyContentFromFile()
				time.sleep(3)
				chatTextAreaPaste()
				time.sleep(2)
				sendMsgButtonClick()
				time.sleep(1)
				
		else:
			urlClick()
			insertUrl(f"wa.me/972{str(phone)}")
			urlContinueClick()
			time.sleep(5)
			continueToChatButtonClick()
			time.sleep(4)
			useWebAppLinkClick()
			time.sleep(60)
			parseNotifContentFromDbToFile("medical")
			copyContentFromFile()
			time.sleep(3)
			chatTextAreaPaste()
			time.sleep(2)
			sendMsgButtonClick()
			time.sleep(1)
			
		sql.execute(f"UPDATE notifier SET last_notif_medic = '{str(datetime.datetime.now())}' WHERE row_id = '{str(notif[0])}'")
		db.commit()


		last_time_master = notif[6]
		if last_time_master not in [None, "None"]:			
			last_time_master = datetime.datetime.strptime(last_time_master, '%Y-%m-%d %H:%M:%S.%f')
			if last_time_master + datetime.timedelta(days=int(notif[4])) < datetime.datetime.now():


				urlClick()
				insertUrl(f"wa.me/972{str(phone)}")
				urlContinueClick()
				time.sleep(10)
				continueToChatButtonClick()
				time.sleep(4)
				useWebAppLinkClick()
				time.sleep(60)
				parseNotifContentFromDbToFile("master")
				copyContentFromFile()
				time.sleep(3)
				chatTextAreaPaste()
				time.sleep(2)
				sendMsgButtonClick()
				time.sleep(1)
				

		else:
			urlClick()
			insertUrl(f"wa.me/972{str(phone)}")
			urlContinueClick()
			time.sleep(10)
			continueToChatButtonClick()
			time.sleep(4)
			useWebAppLinkClick()
			time.sleep(60)
			parseNotifContentFromDbToFile("master")
			copyContentFromFile()
			time.sleep(3)
			chatTextAreaPaste()
			time.sleep(2)
			sendMsgButtonClick()
			time.sleep(1)
			
		sql.execute(f"UPDATE notifier SET last_notif_master = '{str(datetime.datetime.now())}' WHERE row_id = '{str(notif[0])}'")
		db.commit()


		tattoo_time = datetime.datetime.strptime(notif[2], '%Y-%m-%d %H:%M:%S.%f')
		if tattoo_time + datetime.timedelta(weeks=3) < datetime.datetime.now():
			sql.execute(f"DELETE FROM  notifier WHERE row_id = '{str(notif[0])}' WHERE row_id = '{str(notif[0])}'")
			db.commit()



while True:
	try:
		db, sql = db_connector()
		# check notifications
		if datetime.datetime.now().hour in [8, 20]:
			check_notice(db, sql)
		print(str(datetime.datetime.now()).split(".")[0])
		print("[+] Start loop...")
		print("[+] Init callbacks list")
		sql.execute(f"SELECT * FROM callbacks WHERE to_user = '0000'")
		for i in sql.fetchall():
			print("[+] Callback: " + str(i[2]))
			command = i[2].split("||")
			if len(command) == 1:
				command = command[0]
				if command == "start_advert":
					sql.execute(f"SELECT * FROM clients_crm WHERE user_id = '{i[0]}'")
					phones_list = []
					for phones in sql.fetchall():
						phones_list.append(phones[1])

					for phone_num in phones_list:
						sendMessage(phone_num)

						# check notifications
						if datetime.datetime.now().hour in [8, 20]:
							check_notice(db, sql)

					sql.execute(f"DELETE FROM callbacks")
					db.commit()


		try:
		    db.close()
		except:
			pass


		time.sleep(5)
		print("[+] Finish loop")
		print()
	except db_connect.OperationalError:
		print("[-] Error... restart loop...")
		try:
		    db.close()
		except:
			pass
		print()



		

exit()