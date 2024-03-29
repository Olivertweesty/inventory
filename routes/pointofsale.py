from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
from datetime import datetime
import json, ast

db = Database("inventorymanagementsystem","9993revilo")

    

def generateOderID():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d%m%Y%H%M%S")

    return "ZHL-{}".format(timestampStr)


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



def deductQuantity(item):
    sql = "SELECT quantity FROM products WHERE id = '{}'".format(item['item'])
    dquantity = db.selectAllFromtables(sql)[0]['quantity']
    dquantity = int(dquantity) - int(item['quantity'])
    sql = "UPDATE products SET quantity = '{}' WHERE id = '{}'".format(dquantity,item['item'])
    db.updaterecords(sql)

def updateproductsales(product,customer,salesperson,dateT):
    orderitems = product.replace("u'","'")
    items = json.loads(orderitems.replace("'",'"'))

    for item in items:
        sql = "INSERT INTO product_sales VALUES(0,%s,%s,%s,%s,%s,%s,%s)"
        db.insertDataToTable(sql,customer,item['item'],item['price'],item['discount'],item['quantity'],salesperson,dateT)


@routes.route('/submitorder', methods = ["POST"])
def submitorder():
    orderitems = str(request.json.get("orderitems"))
    payment_type = str(request.json.get("payment"))
    customer_id = str(request.json.get("customer_id"))
    transport = str(request.json.get("transport"))
    discount = str(request.json.get("discount"))
    amount_paid = str(request.json.get("amount_paid"))
    installation = str(request.json.get("installation"))
    tax = str(request.json.get("tax"))
    payment_status = ""
    serve_status = str(request.json.get("serve_status"))
    orderID = generateOderID()
    dateTimeObj = datetime.now()
    dateT = dateTimeObj.strftime("%b-%d-%Y %H:%M:%S")
    updateproductsales(orderitems,customer_id,"POS",dateT)
    orderitems = orderitems.replace("u'","'")
    print(orderitems)
    items = json.loads(orderitems.replace("'",'"'))
    #calculate total
    total = 0.0
    for item in items:
        deductQuantity(item)
        total = total + (float(item['quantity']) * float(item['price']))
    #payment-statis
    if payment_type == "Credit":
        payment_status = "credit"
        amount_paid = 0
    elif total > 100000:
        payment_status = "pending"
        amount_paid = 0
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
    sql = "INSERT INTO orders VALUES(0,%s,%s,%s,%s,%s,%s,%s,'pending',%s,%s,%s,%s,%s,%s,'')"
    reponse = db.insertDataToTable(sql,orderID,orderitems,dateT,customer_id,transport,discount,installation,tax,payment_status,total,amount_paid,serve_status,payment_type)
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

def getOnlyRequired(thedate,data):
    totalsale = 0
    unconfirmed = 0
    for order in data:
        order_date = datetime.strptime(order['date_paid'],"%b-%d-%Y %H:%M:%S")
        if order_date.date() == thedate.date():
            if order['confirmed'] == "Confirmed":
                totalsale = totalsale + float(order['amount'])
            else:
                unconfirmed = unconfirmed + float(order['amount'])
            
    return {"totalsale": totalsale,"unconfirmed": unconfirmed}

@routes.route('/getpossummary', methods = ["POST"])
def getpossummary():
    sql = "SELECT * FROM payments"
    response = db.selectAllFromtables(sql)
    dateTimeObj = datetime.now()
    response = getOnlyRequired(dateTimeObj,response)
    return jsonify(response)

@routes.route('/cancelOrder/<id>', methods = ['POST','GET'])
def cancelOrder(id):
    sql = "UPDATE orders SET checkout_status='cancelled' WHERE id = '{}'".format(id)
    response = db.updaterecords(sql)
    if response:
        return jsonify({"response":"Order Cancelled successfully","code":200})
    else:
        return jsonify({"response":"Order Cancelled Failed","code":300})

@routes.route('/confirmpayment', methods = ['POST'])
def confirmpayment():
    orderid = str(request.json.get("orderid"))
    sql = "UPDATE payments SET confirmed ='Confirmed' WHERE id={}".format(orderid)
    response = db.updaterecords(sql)
    if response:
        return jsonify({"response":"Payment Confirmed successfully","code":200})
    else:
        return jsonify({"response":"Payment Confirmation Failed","code":300})


@routes.route('/payments/pos', methods = ['GET'])
def getpospayments():
    sql = "SELECT * FROM payments WHERE served_by ='POS'"
    response = db.selectAllFromtables(sql)

    return jsonify(response)

    





