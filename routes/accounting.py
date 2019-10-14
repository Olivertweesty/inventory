from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
import json
from datetime import datetime
import ast

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


@routes.route('/getaccountsorders/<order_type>',methods = ["POST","GET"])
def getaccountsorders(order_type):
    response = db.selectAllFromtables(tb.selectAllAccountsOrders.format(order_type))
 
    return jsonify(response)

@routes.route('/processpendinginvoice', methods = ["POST"])
def processpending():
	payment_type = str(request.json.get("payment"))
	order_id = str(request.json.get("order_id"))
	discount = str(request.json.get("discount"))
	transport = str(request.json.get("transport"))
	amount_paid = str(request.json.get("amount_paid"))
	serve_status = str(request.json.get("serve_status"))
	inv_type = str(request.json.get("type"))
	dateTimeObj = datetime.now()
	dateT = dateTimeObj.strftime("%b-%d-%Y %H:%M:%S")

	print(amount_paid)
	if payment_type == "Credit":
		payment_status = "credit"
		amount_paid = 0
	else:
		payment_status = "paid"

	date_confirmed,confirmed = "",""
	if payment_type == "Cheque":
		confirmed = "Not Confirmed"
	else:
		date_confirmed = dateT
		confirmed = "Confirmed"

	sql = """UPDATE orders SET 
							transport='{}',discount='{}',payment_status = '{}',total_paid='{}',serve_status='{}',payment_type='{}' 
							WHERE id = '{}'""".format(transport,discount,payment_status,amount_paid,serve_status,payment_type,order_id)
	sql2 = "SELECT orderid,customer_id FROM orders WHERE id='{}'".format(order_id)
	responseO = db.updaterecords(sql)
	response = db.selectAllFromtables(sql2)
	customer_id = response[0]['customer_id']
	orderID = response[0]['orderid']
	details = ""

	
	if inv_type == "credit" or payment_status == "credit":
		pass
	else:
		sql2 = "INSERT INTO payments VALUES(0,%s,%s,%s,%s,%s,%s,'FINANCE',%s,%s)"
		db.insertDataToTable(sql2,orderID,amount_paid,customer_id,payment_type,dateT,date_confirmed,details,confirmed)
	if responseO:
		return jsonify({"response":"successful Placed Order","code":200,"id":order_id})
	else:
		return jsonify({"response":"failed to Place Order","code":300})



@routes.route("/payinvoince", methods=['POST'])
def payinvoice():
	amount_paid = str(request.json.get("amount_paid"))
	order_id = str(request.json.get("order_id"))
	payment_type = str(request.json.get("payment"))
	dateTimeObj = datetime.now()
	dateT = dateTimeObj.strftime("%b-%d-%Y %H:%M:%S")

	date_confirmed,confirmed = "",""
	if payment_type == "Cheque":
		confirmed = "Not Confirmed"
	else:
		date_confirmed = dateT
		confirmed = "Confirmed"

	sql = "SELECT orderid,customer_id,total_paid,total_amount FROM orders WHERE id='{}'".format(order_id)

	response = db.selectAllFromtables(sql)
	print(response)
	customer_id = response[0]['customer_id']
	orderID = response[0]['orderid']
	total_paid = response[0]['total_paid']
	total_amount = response[0]['total_amount']
	details = ""
	payment_status = "credit"

	current_paid = float((total_paid)) + float((amount_paid))
	if current_paid >= float((total_amount)):
		payment_status = "paid"

	sql3 = "UPDATE orders SET total_paid = '{}',payment_status = '{}' WHERE id = '{}'".format(current_paid,payment_status,order_id)
	db.updaterecords(sql3)

	sql2 = "INSERT INTO payments VALUES(0,%s,%s,%s,%s,%s,%s,'FINANCE',%s,%s)"
	response = db.insertDataToTable(sql2,orderID,amount_paid,customer_id,payment_type,dateT,date_confirmed,details,confirmed)

	if response:
		return jsonify({"response":"Payment successful","code":200})
	else:
		return jsonify({"response":"payment failed","code":300})

@routes.route('/payments/finance', methods = ['GET'])
def getfinancepayments():
	sql = "SELECT * FROM payments WHERE served_by ='FINANCE'"
	response = db.selectAllFromtables(sql)

	return jsonify(response)

@routes.route('/getexpensetotal', methods = ['POST'])
def getexpensetotal():
	sql = "SELECT * FROM expenses WHERE status='accepted'"
	response = db.selectAllFromtables(sql)
	total = 0.0
	for item in response:
		if item['type'] == 'credit':
			total = total + float(item['amount'])
		else:
			total = total - float(item['amount'])
	return str(total)


@routes.route("/getgeneralreport", methods = ['POST'])
def getgeneralreport():
	sql = "SELECT * FROM expenses WHERE status='accepted'"
	response = db.selectAllFromtables(sql)
	total_cash_in,total_cash_out, amount_in_finance,amount_in_pos = 0.0,0.0,0.0,0.0
	responsedata =  []
	count = 1
	for item in response:
		data = {"id":count}
		if item['type'] == 'credit':
			total_cash_in = total_cash_in + float(item['amount'])
			amount_in_finance = amount_in_finance + float(item['amount'])
			data['description'] = "Credit - {}".format(item['use'])
			data['amount'] = item['amount']
			data['type'] = "Credit"

		else:
			total_cash_in = total_cash_in - float(item['amount'])
			total_cash_out = total_cash_out + float(item['amount'])
			amount_in_finance = amount_in_finance - float(item['amount'])
			data['description'] = "Debit - {}".format(item['use'])
			data['amount'] = item['amount']
			data['type'] = "Debit"
		responsedata.append(data)
		count = count +1

	sql2 = "SELECT * FROM payments"
	response = db.selectAllFromtables(sql2)

	for item in response:
		data = {"id":count}
		if item['served_by'] == "POS":
			total_cash_in = total_cash_in + float(item['amount'])
			amount_in_pos = amount_in_pos + float(item['amount'])
			data['description'] = "Sale - {} paid via {}".format(item['invoice_id'],item['payment_type'])
			data['amount'] = item['amount']
			data['type'] = "Sales"
		else:
			total_cash_in = total_cash_in + float(item['amount'])
			amount_in_finance = amount_in_finance + float(item['amount'])
			data['description'] = "Sale - {} paid via {}".format(item['invoice_id'],item['payment_type'])
			data['amount'] = item['amount']
			data['type'] = "Sales"
		count = count + 1
		responsedata.append(data)

	response = {"total_cash_in": total_cash_in,
				"total_cash_out":total_cash_out,
				"amount_in_finance":amount_in_finance,
				"amount_in_pos":amount_in_pos,
				"other":responsedata
				}
	return jsonify(response)

