from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
from datetime import datetime

db = Database("inventorymanagementsystem","9993revilo")

    

def generateOderID():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d%m%Y%H%M%S")

    return "ORD-{}".format(timestampStr)


@routes.route('/pointofsale')
def pointofsale():
    return render_template("pos_main.html")

@routes.route('/getposproducts',methods = ["POST","GET"])
def getposproducts():
    response = db.selectAllFromtables(tb.selectproductPOS)

    return jsonify(response)

@routes.route('/addcustomer',methods = ["POST","GET"])
def addcustomer():
    name = str(request.json.get("name"))
    co_name = str(request.json.get("company_name"))
    mobile_num = str(request.json.get("mobile_number"))

    sql = "INSERT INTO customers VALUES(0,%s,%s,%s)"

    reponse = db.insertDataToTable(sql,name,co_name,mobile_num)
    print(reponse)
    if reponse:
        return jsonify({"response":"successful added customer","code":200})
    else:
        return jsonify({"response":"failed to add customer","code":300})


@routes.route('/submitorder', methods = ["POST"])
def submitorder():
    orderitems = str(request.json.get("orderitems"))
    payment_type = str(request.json.get("payment"))
    customer_id = str(request.json.get("customer_id"))
    transport = str(request.json.get("transport"))
    discount = str(request.json.get("discount"))
    orderID = generateOderID()
    dateTimeObj = datetime.now()
    dateT = dateTimeObj.strftime("%b-%d-%Y %H:%M:%S")

    sql = "INSERT INTO orders VALUES(0,%s,%s,%s,%s,%s,%s,%s,'')"
    reponse = db.insertDataToTable(sql,orderID,orderitems,payment_type,dateT,customer_id,transport,discount)

    if reponse:
        return jsonify({"response":"successful Placed Order","code":200})
    else:
        return jsonify({"response":"failed to Place Order","code":300})


