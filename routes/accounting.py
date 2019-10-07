from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
import json
from datetime import datetime

db = Database("inventorymanagementsystem","9993revilo")

@routes.route('/account')
def account():
    return render_template("account_main.html")

@routes.route("/addexpense",methods = ['POST','GET'])
def addexpense():
	date = str(request.json.get("date"))
	use = str(request.json.get("use"))
	amount = str(request.json.get("amount"))
	ex_type = str(request.json.get("type"))

	sql = "INSERT INTO expenses VALUES(0,%s,%s,%s,%s,%s)"

	reponse = db.insertDataToTable(sql,date,use,amount,ex_type,"pending")
	if reponse:
		return jsonify({"response":"successful added expense","code":200})
	else:
		return jsonify({"response":"failed to add expense","code":300})
@routes.route("/getexpenses", methods = ['GET'])
def getexpenses():
	sql = "SELECT * FROM expenses"
	response = db.selectAllFromtables(sql)
	return jsonify(response)

@routes.route("/processExpense/<id_>/<what>", methods = ['POST','GET'])
def processExpense(id_,what):
	sql2 = "UPDATE expenses SET status='{}' WHERE id = '{}'".format(what,id_)
	response = db.updaterecords(sql2)
	if response:
		return jsonify({"response":"successful processed Expense","code":200})
	else:
		return jsonify({"response":"failed to process Expense","code":300})
