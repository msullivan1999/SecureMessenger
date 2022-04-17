import sqlite3
import hashlib
import secrets

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
	'''
	  Our SQL Database

	'''

	# Get the database running
	def __init__(self, database_arg=":memory:"):
		self.current_id = 0
		self.conn = sqlite3.connect(database_arg)
		self.cur = self.conn.cursor()
		
		# set up the database file: clear all & insert new admin in
		self.database_setup()

	# SQLite 3 does not natively support multiple commands in a single statement
	# Using this handler restores this functionality
	# This only returns the output of the last command
	def execute(self, sql_string):

		out = None
		for string in sql_string.split(";"):
			try:
				out = self.cur.execute(string)
			except:
				print("{} unsuccessful".format(string))
		
		# commit the database state to save the transaction
		self.commit()
		
		return out

	# Commit changes to the database
	def commit(self):
		self.conn.commit()

	#-----------------------------------------------------------------------------

	# Sets up the database
	# Default admin password
	def database_setup(self, admin_password='admin'):

		# Clear the db
		self.execute("DROP TABLE IF EXISTS Users")
		self.execute("DROP TABLE IF EXISTS Pubkeys")
		self.execute("DROP TABLE IF EXISTS Messages")
		self.execute("DROP TABLE IF EXISTS UserFriends")

		self.commit()

		# Create the users table
		self.execute("""CREATE TABLE Users(
			Id INT,
			username TEXT,
			password_hash TEXT,
			salt TEXT,
			admin INTEGER DEFAULT 0
		)""")

		self.execute('''CREATE TABLE Pubkeys(
			public_key INT,
			username TEXT
		)''')

		self.execute('''CREATE TABLE Messages (
			sender_pub_key INT,
			nonce INT,
			message TEXT
		)''')

		# The 'user' acts as a primary key
		# and maps to the users in the 'Users' table
		self.execute('''CREATE TABLE UserFriends (
			user TEXT,
			friend TEXT
		)''')

		self.commit()

		# Add our admin user
		self.add_user(username='admin', password=admin_password, admin=1)

	#-----------------------------------------------------------------------------
	# User handling
	#-----------------------------------------------------------------------------

	# Add a user to the database
	# hashes the input password with an associated salt
	# store h(pwd || salt), salt (plaintext)
	def add_user(self, username, password, admin=0):

		sql_cmd = """
				 INSERT INTO Users
				 VALUES({Id}, '{username}', '{password_hash}', '{salt}', {admin})
			"""

		m = hashlib.sha256() # 256 hash algo
		salt = secrets.token_hex(8) # salt str
		# concatenate string, encode, hash
		m.update((password + salt).encode())
		pwd_salt_hash = m.hexdigest()
		
		sql_cmd = sql_cmd.format(
			Id=self.current_id, username=username, 
			password_hash=pwd_salt_hash, salt=salt, 
			admin=admin)

		self.execute(sql_cmd)
		self.commit()
		self.current_id += 1
		
		return True

	#-----------------------------------------------------------------------------
	# Adding usr public key
	#-----------------------------------------------------------------------------
	def add_user_key(self, username, pub_key):
		sql_cmd='''
			INSERT INTO Pubkeys
			VALUES({public_key}, '{username}')
		'''

		sql_cmd = sql_cmd.format(username=username, public_key=pub_key)

		self.execute(sql_cmd)
		self.commit()

	#-----------------------------------------------------------------------------

	# Check login credentials
	# get the salt from the user
	# append to password & hash
	# compare hashes
	def check_credentials(self, username, password):

		sql_query = """
				 SELECT *
				 FROM Users
				 WHERE username = '{username}'
			"""

		sql_query = sql_query.format(username=username)
		
		self.execute(sql_query)
		rows = self.cur.fetchall()

		# no such user
		if rows == None or len(rows) == 0:
			return False

		# user exists
		# [(uid, usr, h(pwd+salt), salt, admin)]
		# extract the expected digest & salt
		expected = rows[0][2]
		salt = rows[0][3]
		
		m = hashlib.sha256()

		m.update((password + salt).encode())
		input_digest = m.hexdigest()
		
		# if the digest from input matches the 
		# digest from the stored pwd & salt
		if expected == input_digest:
			return True
		return False

	def get_pub_key(self, usr):
		'''
			get public key of a user from username
		'''

		query = '''
			SELECT public_key FROM Pubkeys WHERE username = '{usr}'
		'''
		query = query.format(usr=usr)
		self.execute(query)
		rows = self.cur.fetchall()
		return rows

	def get_users(self):
		'''
			Retrieve list of all users from database
		'''

		sql_query = 'SELECT username FROM Users WHERE admin=0'
		self.execute(sql_query)
		rows = self.cur.fetchall()
		return rows


	def add_to_friends(self, usr_a, usr_b):

		'''
			add usr_b into usr_a's friends ls
		'''

		cmd = '''
			INSERT INTO UserFriends VALUES('{user_a}' , '{user_b}')
		'''
		# add b into a's friends ls
		cmd = cmd.format(user_a=usr_a, user_b=usr_b)
		self.execute(cmd)

		# add a into b's friends ls (bidirectional)
		cmd = cmd.format(user_a=usr_a, user_b=usr_b)
		self.execute(cmd)


	def insert_message(self, ciphertext, nonce, sender_public_key):
		''' insert ciphertext into Messages table '''
		pass
		
	def get_message(self, sender_pub_key):
		sql_query = ''
		messages = [] # list of messages here
		return messages
		
		
