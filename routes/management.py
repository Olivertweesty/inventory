from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
import requests
import json
from datetime import datetime

db = Database("inventorymanagementsystem","9993revilo")

@routes.route('/management')
def management():
    return render_template("head_dashboard.html")


def getItemNameByID(id):
    sql = tb.selectProductnameById.format(id)
    response = db.selectAllFromtables(sql)
    return response[0]
@routes.route("/getsystemusers", methods = ["POST","GET"])
def getSystemUsers():
    sql = "SELECT u.id, e.firstname,u.phone,u.access_rights,u.username FROM users AS u JOIN employees AS e ON u.userid = e.id"
    response = db.selectAllFromtables(sql)
    return jsonify(response)

@routes.route("/addsystemuser", methods = ["POST","GET"])
def addSystemUsers():
	userid = str(request.json.get("userid"))
	username = str(request.json.get("username"))
	phone = str(request.json.get("phone"))
	access_rights = str(request.json.get("access_rights"))
	password = str(request.json.get("password"))

	data = {
		"message":"You Have been Registered as system user use The follwing Cridentials to log in\nUsername : {} \nPassword: {}\n You can Access :{}".format(username,password,access_rights),
		"phone_number":phone
	}
	url = "https://backend.security.riwaa.co.ke/api/sendSmsTest"
	sql = "INSERT INTO users VALUES(0,%s,%s,%s,%s,%s)"
	reponse = db.insertDataToTable(sql,userid,username,access_rights,phone,password)
	if reponse:
		requests.post(url,json=data)
		return jsonify({"response":"successful added user","code":200})
	else:
		return jsonify({"response":"failed to add user","code":300})

def getPayedAndNot(data):
	totalsales = 0.0
	totaloncredit = 0.0
	totalpaid = 0.0
	for item in data:
		items = item['items']
		items = json.loads(items.replace("'",'"'))
		for each in items:
			 totalsales = totalsales + float(each['price']) * int(each['quantity'])

	for item in data:
		if item['payment_type'] == "Credit":
			items = item['items']
			
			items = json.loads(items.replace("'",'"'))
			for each in items:
				 totaloncredit = totaloncredit + float(each['price']) * int(each['quantity'])
	totalpaid = totalsales - totaloncredit
	return {"totalsale":totalsales,"oncredit":totaloncredit,"paid":totalpaid,"sales":len(data)}

def getOnlyRequired(thedate,data):
	data_to_return = []
	for order in data:
		order_date = datetime.strptime(order['date'],"%b-%d-%Y %H:%M:%S")
		if order_date.date() == thedate.date():
			data_to_return.append(order)
	return data_to_return

@routes.route("/getdailyreport", methods = ["POST","GET"])
def getdailyreport():
	thedate = str(request.json.get("thedate"))
	datetime_object = datetime.strptime(thedate, '%Y-%m-%d')
	
	sql = "SELECT items,date,payment_type FROM orders"
	response = getOnlyRequired(datetime_object, db.selectAllFromtables(sql))
	items_to_return = []
	count = 1
	other = getPayedAndNot(response)
	for item in response:
		items = item['items']
		items = json.loads(items.replace("'",'"'))
		the_items = {}
		
		for each in items:
			item_name = getItemNameByID(each['item'])['product_name']
			the_items['id'] = count
			the_items['item_name'] = item_name
			the_items['quantity'] = each['quantity']
			the_items['price_per_item'] = each['price']
			the_items['total'] = float(each['price']) * int(each['quantity'])
		count = count + 1
		items_to_return.append(the_items)

	return jsonify({"table_data":items_to_return,"other":other})
