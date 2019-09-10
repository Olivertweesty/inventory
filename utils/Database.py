import pymysql.cursors
import json
import utils.tables as tb

class Database:
	def __init__(self, databasename):
		self.databasename = databasename
		#Creating the database if it does not exist
		connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		cursor = connection.cursor()

		cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(databasename))
		connection.commit()
		connection.close()
		self.createtables()

	def connectToDatabase(self):
		connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db=self.databasename,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
		return connection

	def createtables(self):
		conn = self.connectToDatabase()
		cursor = conn.cursor()
		cursor.execute(tb.appusers)
		cursor.execute(tb.products)
		cursor.execute(tb.product_names)
		cursor.execute(tb.manufacterer)
		conn.commit()
		conn.close()
	
	def selectSpecificItemsFromDb(self,table,and_or, **kwargs):
		"""This method takes the name of a table, and the agurments of a where clause
		builds an sql statement, Query for data then returns the results"""

		values = tuple([value for key, value in kwargs.items()])
		
		conn = self.connectToDatabase()
		cursor = conn.cursor()
		sql = "SELECT * FROM {} WHERE ".format(table)
		count = 0
		for key, value in kwargs.items():
			if count == 0:
				sql = sql+key+" = %s "
			else:
				sql = sql+and_or+" "+key+" = %s "
			count = count + 1
		
		cursor.execute(sql,values)
		response = cursor.fetchall()
		return response



	def insertDataToTable(self,sql,*args):
		"""This method is used to enter data into a table"""
		values = tuple([value for  value in args])
		
		try:
			conn = self.connectToDatabase()
			cursor = conn.cursor()
			cursor.execute(sql,values)
			conn.commit()
		except:
			return False

		return True

	def selectAllFromtables(self,table):
		sql = "SELECT * FROM {}".format(table)
		try:
			conn = self.connectToDatabase()
			cursor = conn.cursor()
			cursor.execute(sql)
			response = cursor.fetchall()
			conn.commit()
			return response
		except:
			return False
			
			

		