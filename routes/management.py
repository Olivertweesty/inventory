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
