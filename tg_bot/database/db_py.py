import sqlite3
import time
from datetime import datetime, date


# класс взаимодействия с базой данных
class database_management():
	# Используется
	# Функция запускатся при старте
	def __init__(self):
		self.db_1 = sqlite3.connect('tg_bot\\database\\users.db', check_same_thread=False)

		self._create_db_users()
		self._create_db_links()


	# Используется
	# Создаем базу пользователей db_1
	def _create_db_users(self):
		# cursor() позволяет делать sql запросы
		self.sql_1 = self.db_1.cursor()

		# Создаем таблицу если она не создана users - название таблицы
		self.sql_1.execute("""CREATE TABLE IF NOT EXISTS users (
		ID INT, 
		NAME TEXT, 
		LINK TEXT,
		NUM_PROD INT,
		SUBSCRIBE TEXT,
		TIME TEXT,
		TIME_REG TEXT
		)""")

		# ID        - id пользователя
		# NAME      - имя
		# LINK      - @link
		# NUM_PROD 	- количество отслеживаемых товаров
		# SUBSCRIBE - Статус подписки на бота
		# TIME 		- До какого числа подписка

		# Подтверждаем сохранение
		self.db_1.commit()


	# Используется
	# Создаем базу хранящую id, links
	def _create_db_links(self):
		# cursor() позволяет делать sql запросы
		self.sql_2 = self.db_1.cursor()

		# Создаем таблицу если она не создана LINKS - название таблицы
		self.sql_2.execute("""CREATE TABLE IF NOT EXISTS USLINKS (
		ID INT, 
		LINKS TEXT,
		HIST_LINKS TEXT
		)""")

		# ID        - id пользователя
		# LINKS     - Картетж ссылок

		# Подтверждаем сохранение
		self.db_1.commit()


	def _create_db_pay(self):
		# cursor() позволяет делать sql запросы
		self.sql_3 = self.db_1.cursor()

		# Создаем таблицу если она не создана LINKS - название таблицы
		self.sql_3.execute("""CREATE TABLE IF NOT EXISTS USLINKS (
		PID INT,
		ID INT, 
		BILL TEXT,
		COMMENT TEXT,
		TIME INT,
		D_TIME TEXT,
		STATUS TEXT
		)""")

		# PID		- Последовательный номер
		# ID 		- id оплачивающего
		# BILL 		- номер оплаты
		# COMMENT 	- коментарий
		# TIME 		- unix врмея выставления платежа
		# D_TIME 	- время выставления платежа
		# STATUS 	- статус оплаты True/False

		# Подтверждаем сохранение
		self.db_1.commit()


	# Используется
	# Проверить наличие пользователя в базе
	def check_the_user(self, user_id: int, user_name: str, user_link: str) -> bool:
		# Выбрать столбел ID в таблице users, где ID равен = user_login
		self.sql_1.execute(f"SELECT ID FROM users WHERE ID = '{user_id}'")

		# Если такого KEY нету в базе, то
		if self.sql_1.fetchone() is None:
			# Текущая дата
			current_date = date.today()

			# Текущее время
			tek_ti = time.time()
			# К текущему времени добавляем 24 часа
			ti_new = int(tek_ti) + int(259200)

			# Добавим запись в базу данных людей
			self.sql_1.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, user_name, user_link, 0, 'False', ti_new, current_date))

			# Добавим запись в базу данных ссылок
			self.sql_2.execute(f"INSERT INTO USLINKS VALUES (?, ?, ?)", (user_id, '', ''))

			# подтвердим сохранение
			self.db_1.commit()

			# Раньше его не было
			return False

		# Если ключ есть в базе
		else:
			# Раньше он был
			return True


	# Используется
	# Проверяем есть ли пользователь в базе
	def check_user_in_db(self, user_id):
		try:
			# Проверка наличия
			self.sql_1.execute(f"SELECT ID FROM users WHERE ID = '{user_id}'")
			user_id_in_db = self.sql_1.fetchone()[0]

			return "Good"
		except Exception:
			return "Error"


	# Поверка согласия с правилами
	def verification_of_consent(self, user_id: int) -> str:
		# Читаем IAGREE из таблицы users, где ID равн user_id
		self.sql_1.execute(f"SELECT IAGREE FROM users WHERE ID = '{user_id}'")
		user_iagree_status = self.sql_1.fetchone()[0]

		return user_iagree_status


	# Проверка наличия бана
	def checking_the_black_spike(self, user_id: int) -> str:
		# Читаем BLACKL из таблицы users, где ID равн user_id
		self.sql_1.execute(f"SELECT BLACKL FROM users WHERE ID = '{user_id}'")
		user_ban_status = self.sql_1.fetchone()[0]

		return user_ban_status


	# указываем что пользователь согласен с правилами
	def iagree(self, user_id: int) -> None:
		# Обновить в таблице users, добавить в столбце IAGREE новое значение, где столбец IAGREE равен = user_id
		self.sql_1.execute(f'UPDATE users SET IAGREE = "{True}" WHERE ID = "{user_id}"')
		# Подтвердили изменения
		self.db_1.commit()


	# Заблокировать пользователя
	def ban_user(self, user_id):
		try:
			# Проверка наличия
			self.sql_1.execute(f"SELECT BLACKL FROM users WHERE ID = '{user_id}'")
			user_ban_status = self.sql_1.fetchone()[0]

			# Обновить в таблице users, добавить в столбце BLACKL новое значение, где столбец ID равен = False
			self.sql_1.execute(f'UPDATE users SET BLACKL = "True" WHERE ID = "{user_id}"')
			self.db_1.commit()  # Подтвердили изменения

			return "Good"
		except Exception:
			return "Error"


	# Узнаем количество людей в базе
	def info_nums_user(self):
		# Читаем ID из таблицы users
		self.sql_1.execute(f"SELECT ID FROM users")
		nums = self.sql_1.fetchall()

		return len(nums)


	# Получаем список id всех пользователей из базы
	def list_user_id(self):
		# Читаем ID из таблицы users
		self.sql_1.execute(f"SELECT ID FROM users")
		nums = self.sql_1.fetchall()

		return nums


	# Используется
	# Переделан
	# Получаем информацию о профиле
	def get_my_profil(self, user_id):
		try:
			# Читаем NAME из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT NAME FROM users WHERE ID = '{user_id}'")
			us_name = self.sql_1.fetchone()[0]

			# Читаем LINK из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT LINK FROM users WHERE ID = '{user_id}'")
			us_link = self.sql_1.fetchone()[0]

			# Читаем NUM_PROD из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT NUM_PROD FROM users WHERE ID = '{user_id}'")
			us_num_prod = self.sql_1.fetchone()[0]

			# Читаем SUBSCRIBE из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT SUBSCRIBE FROM users WHERE ID = '{user_id}'")
			us_subs = self.sql_1.fetchone()[0]

			# Читаем TIME из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT TIME FROM users WHERE ID = '{user_id}'")
			us_time = self.sql_1.fetchone()[0]

			return us_name, us_link, us_num_prod, us_subs, us_time
		except:
			return "Error", "Error", "Error", "Error", "Error"


	# Разблокировать пользователя
	def unban_user(self, user_id):
		try:
			# Обновить в таблице users, добавить в столбце BLACKL новое значение, где столбец ID равен = False
			self.sql_1.execute(f'UPDATE users SET BLACKL = "False" WHERE ID = "{user_id}"')
			self.db_1.commit()  # Подтвердили изменения

			return "Good"
		except Exception:
			return "Error"


	# Узнаем количество людей в базе
	def info_nums_user(self):
		# Читаем ID из таблицы users
		self.sql_1.execute(f"SELECT ID FROM users")
		nums = self.sql_1.fetchall()

		return len(nums)


	# Получаем список id всех пользователей из базы
	def list_user_id(self):
		# Читаем ID из таблицы users
		self.sql_1.execute(f"SELECT ID FROM users")
		nums = self.sql_1.fetchall()

		return nums


	# Получаем информацию о профиле
	def my_profil(self, user_id):
		try:
			# Читаем NAME из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT NAME FROM users WHERE ID = '{user_id}'")
			us_name = self.sql_1.fetchone()[0]

			# Читаем LINK из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT LINK FROM users WHERE ID = '{user_id}'")
			us_link = self.sql_1.fetchone()[0]

			# Читаем BALANCE из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT BALANCE FROM users WHERE ID = '{user_id}'")
			us_balance = self.sql_1.fetchone()[0]

			# Читаем BLACKL из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT BLACKL FROM users WHERE ID = '{user_id}'")
			us_st_black = self.sql_1.fetchone()[0]


			return us_name, us_link, us_balance, us_st_black
		except Exception:
			return "Error", "Error", "Error", "Error"


	# Получаем список ссылок из базы
	def get_my_list_links(self, user_id):
		# Читаем LINKS из таблицы LINKS, где ID равен user_id
		self.sql_1.execute(f"SELECT LINKS FROM USLINKS WHERE ID = '{user_id}'")
		us_links = self.sql_1.fetchone()[0]

		return us_links


	# Получаем список просмотренных ссылок из базы
	def get_my_list_hist_links(self, user_id):
		# Читаем HIST_LINKS из таблицы LINKS, где ID равен user_id
		self.sql_1.execute(f"SELECT HIST_LINKS FROM USLINKS WHERE ID = '{user_id}'")
		us_links = self.sql_1.fetchone()[0]

		return us_links

	# Добавляем ссылку в базу
	def add_hist_links_in_db(self, user_id, link):
		try:
			# Читаем HIST_LINKS из таблицы LINKS, где ID равен user_id
			self.sql_2.execute(f"SELECT HIST_LINKS FROM USLINKS WHERE ID = '{user_id}'")
			us_links = self.sql_2.fetchone()[0]

			us_links += ", " + str(link)

			# Обновить в таблице USLINKS, добавить в столбце HIST_LINKS новое значение, где столбец ID равен = user_id
			self.sql_2.execute(f'UPDATE USLINKS SET HIST_LINKS = "{us_links}" WHERE ID = "{user_id}"')
			self.db_1.commit()  # Подтвердили изменения

			return "Good"
		except Exception:
			return "Error"


	# Добавляем ссылку в базу
	def add_links_in_db(self, user_id, link):
		try:
			# Читаем LINKS из таблицы LINKS, где ID равен user_id
			self.sql_2.execute(f"SELECT LINKS FROM USLINKS WHERE ID = '{user_id}'")
			us_links = self.sql_2.fetchone()[0]

			us_links += ", " + str(link)

			# Обновить в таблице users, добавить в столбце BLACKL новое значение, где столбец ID равен = False
			self.sql_2.execute(f'UPDATE USLINKS SET LINKS = "{us_links}" WHERE ID = "{user_id}"')

			# Читаем NUM_PROD из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT NUM_PROD FROM users WHERE ID = '{user_id}'")
			us_num_prod = self.sql_1.fetchone()[0]
			us_num_prod = int(us_num_prod) + 1


			self.sql_1.execute(f"UPDATE users SET NUM_PROD = '{us_num_prod}' WHERE ID = '{user_id}'")

			self.db_1.commit()  # Подтвердили изменения

			return "Good"
		except Exception as e:
			print(e)
			return "Error " + str(e)


	# удалить ссылку из базу
	def del_links_in_db(self, user_id, link_num):
		try:
			# Читаем LINKS из таблицы LINKS, где ID равен user_id
			self.sql_2.execute(f"SELECT LINKS FROM USLINKS WHERE ID = '{user_id}'")
			us_links = self.sql_2.fetchone()[0]

			lst = us_links.replace(',', '').split()

			lst.pop(int(link_num))

			us_links = ", ".join(lst)

			# Обновить в таблице users, добавить в столбце BLACKL новое значение, где столбец ID равен = False
			self.sql_2.execute(f'UPDATE USLINKS SET LINKS = "{us_links}" WHERE ID = "{user_id}"')

			# Читаем NUM_PROD из таблицы users, где ID равен user_id
			self.sql_1.execute(f"SELECT NUM_PROD FROM users WHERE ID = '{user_id}'")
			us_num_prod = self.sql_1.fetchone()[0]

			if int(us_num_prod) != 0:
				us_num_prod = int(us_num_prod) - 1

			self.sql_1.execute(f"UPDATE users SET NUM_PROD = '{us_num_prod}' WHERE ID = '{user_id}'")

			self.db_1.commit()  # Подтвердили изменения

			return "Good"
		except Exception as e:
			return "Error"


	# Получить список всех id
	def get_all_id_user(self):
		# Читаем ID из таблицы USLINKS
		self.sql_2.execute(f"SELECT ID FROM USLINKS")
		list = []

		for i in self.sql_2.fetchall():
			#print(i[0])
			list.append(i[0])

		#us_id = self.sql_2.fetchall()

		return list


	# Узнать до какого подписка
	def get_time_subscribe(self, user_id):
		# Читаем TIME из таблицы users, где ID равен user_id
		self.sql_1.execute(f"SELECT TIME FROM users WHERE ID = '{user_id}'")
		us_time = self.sql_1.fetchone()[0]

		return us_time