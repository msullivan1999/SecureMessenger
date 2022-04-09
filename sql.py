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

		# Clear the database if needed
		self.execute("DROP TABLE IF EXISTS Users")
		self.commit()

		# Create the users table
		self.execute("""CREATE TABLE Users(
			Id INT,
			username TEXT,
			password_hash TEXT,
			salt TEXT,
			admin INTEGER DEFAULT 0
		)""")

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
		if rows == None:
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







