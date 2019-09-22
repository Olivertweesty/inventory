from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
import json

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
    sql = "SELECT id, name, email,phone,access_rights,username FROM users"
    response = db.selectAllFromtables(sql)
    return jsonify(response)


@routes.route("/addsystemuser", methods = ["POST","GET"])
def addSystemUsers():
	username = str(request.json.get("username"))
	name = str(request.json.get("full_name"))
	phone = str(request.json.get("phone"))
	access_rights = str(request.json.get("access_rights"))
	password = str(request.json.get("password"))
	gender = str(request.json.get("gender"))
	email = str(request.json.get("email"))
    
	sql = "INSERT INTO users VALUES(0,%s,%s,%s,%s,%s,%s,%s)"
	reponse = db.insertDataToTable(sql,name,email,username,access_rights,phone,gender,password)
	if reponse:
		return jsonify({"response":"successful added user","code":200})
	else:
		return jsonify({"response":"failed to add user","code":300})

@routes.route("/getdailyreport", methods = ["POST","GET"])
def getdailyreport():
	sql = "SELECT items FROM orders"
	response = db.selectAllFromtables(sql)
	items_to_return = []
	count = 1
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

	return jsonify(items_to_return)
