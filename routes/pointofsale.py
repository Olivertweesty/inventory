from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
from datetime import datetime
import json

db = Database("inventorymanagementsystem","9993revilo")

    

def generateOderID():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d%m%Y%H%M%S")

    return "INV-{}".format(timestampStr)


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
    amount_paid = str(request.json.get("amount_paid"))
    payment_status = ""
    serve_status = str(request.json.get("serve_status"))
    orderID = generateOderID()
    dateTimeObj = datetime.now()
    dateT = dateTimeObj.strftime("%b-%d-%Y %H:%M:%S")

    items = json.loads(orderitems.replace("'",'"'))
    #calculate total
    total = 0
    for item in items:
        total = total + (float(item['quantity']) * float(item['price']))
    #payment-statis
    if payment_type == "Credit":
        payment_status = "credit"
    else:
        payment_status = "paid"

    date_confirmed,confirmed = "",""
    if payment_type == "Cheque":
        confirmed = "Not Confirmed"
    else:
        date_confirmed = dateT
        confirmed = "Confirmed"

    details = ""


    sqlID = "SELECT MAX(id) FROM orders"
    sql2 = "INSERT INTO payments VALUES(0,%s,%s,%s,%s,%s,%s,'POS',%s,%s)"
    sql = "INSERT INTO orders VALUES(0,%s,%s,%s,%s,%s,%s,'pending',%s,%s,%s,%s,%s,'')"
    reponse = db.insertDataToTable(sql,orderID,orderitems,dateT,customer_id,transport,discount,payment_status,total,amount_paid,serve_status,payment_type)
    responseISD = db.selectAllFromtables(sqlID)
    if serve_status == "pending" or payment_status == "credit":
        pass
    else:
        db.insertDataToTable(sql2,orderID,amount_paid,customer_id,payment_type,dateT,date_confirmed,details,confirmed)
    print(responseISD)
    if reponse:
        return jsonify({"response":"successful Placed Order","code":200,"id":responseISD[0]['MAX(id)']})
    else:
        return jsonify({"response":"failed to Place Order","code":300})


@routes.route('/getallposorders',methods = ["POST","GET"])
def getallPosorders():
    response = db.selectAllFromtables(tb.selectAllOrders)

    return jsonify(response)

@routes.route('/cancelOrder/<id>', methods = ['POST','GET'])
def cancelOrder(id):
    sql = "UPDATE orders SET status='cancelled' WHERE id = '{}'".format(id)
    response = db.updaterecords(sql)
    if response:
        return jsonify({"response":"Order Cancelled successfully","code":200})
    else:
        return jsonify({"response":"Order Cancelled Failed","code":300})


@routes.route('/payments/pos', methods = ['GET'])
def getpospayments():
    sql = "SELECT * FROM payments WHERE served_by ='POS'"
    response = db.selectAllFromtables(sql)

    return jsonify(response)





