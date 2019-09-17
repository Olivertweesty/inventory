from flask import render_template
from . import routes
from flask import jsonify
from flask import request
from utils.Database import Database
import utils.tables as tb
from datetime import date

db = Database("inventorymanagementsystem","9993revilo")

@routes.route('/warehouse')
def warehouse():
    return render_template("warehouse_dashboard.html")

@routes.route('/<name>')
def warehousepages(name):
    if name == "warehouse_checkin":
        return render_template("warehouse_checkin.html")
    elif name == "warehouse_damage":
        return render_template("warehouse_damage.html")
    elif name == "warehouse_allproducts":
        return render_template("warehouse_allproducts.html")
    elif name == "stock_taking":
        return render_template("warehouse_stocktaking.html")
    elif name == "pending_orders":
        return render_template("warehouse_pending_order.html")
    else:
        return render_template("404.html")



@routes.route('/checkinproducts',methods = ["POST"])
def checkin_products():
    manufacterer = str(request.json.get("manufacterer"))
    productname = str(request.json.get("productname"))
    unit_of_measument = str(request.json.get("unit_of_measument"))
    quantity = str(request.json.get("quantity"))
    purchase_price = str(request.json.get("purchase_price"))
    print("Hello")
    product_code = (manufacterer[0:4]+productname[0:4])

    existance = db.selectSpecificItemsFromDb("products","AND",product_code=product_code,manufacturer=manufacterer,product_name=productname)
    if len(existance) == 0:
        sql = "INSERT INTO products VALUES(0,%s,%s,%s,%s,%s,'',%s)"
        reponse = db.insertDataToTable(sql,product_code,manufacterer,productname,purchase_price,unit_of_measument,quantity)
    else:
        new_quantity = existance[0]['quantity'] + quantity
        sql = "UPDATE products SET quantity = %s"
        response = db.insertDataToTable(sql,new_quantity)

    if reponse == True:
        return jsonify({"response":"successful product Checkin","code":200})
    else:
        return jsonify({"response":"failed to checkin product","code":300})



@routes.route('/addproductname',methods = ["POST"])
def addproductname():
    product_name = str(request.json.get("productname"))
    
    sql = "INSERT INTO products_name VALUES(0,%s)"
    reponse = db.insertDataToTable(sql,product_name)
    print(reponse)
    if reponse:
        return jsonify({"response":"successful added Manufacterer","code":200})
    else:
        return jsonify({"response":"failed to add Manufacterer","code":300})



@routes.route('/addmanufacturername',methods = ["POST"])
def addmanufacturername():
    manufacturer_name = str(request.json.get("manufacturer_name"))
    
    sql = "INSERT INTO manufacterer VALUES(0,%s)"
    reponse = db.insertDataToTable(sql,manufacturer_name)
    print(reponse)
    if reponse:
        return jsonify({"response":"successful added product","code":200})
    else:
        return jsonify({"response":"failed to add product","code":300})



@routes.route('/getdatafromtable/<name>',methods = ["POST"])
def getdatafromtable(name):
    sql = "SELECT * FROM {}".format(name)
    response = db.selectAllFromtables(sql)

    if not response:
        return jsonify({"response":"failed to retrieve data","code":300})
    else:
        return jsonify({"response":response,"code":300})



@routes.route('/getallproducts',methods = ["POST","GET"])
def getallproducts():
    response = db.selectAllFromtables(tb.selectallproduct)

    return jsonify(response)

@routes.route('/getallorders',methods = ["POST","GET"])
def getsingleorders():
    response = db.selectAllFromtables(tb.selectOrdersPending)

    return jsonify(response)

@routes.route('/getsingleorder/<id>',methods = ["POST","GET"])
def getallorders(id):
    sql = "SELECT orderid,items FROM orders WHERE id = '{}'".format(id)
    response = db.selectAllFromtables(sql)
    ids = [x for x in response[0]['items']]
    print(ids)
    #sql2 = "SELECT product_name FROM products WHERE id IN {}".format(ids)

    return jsonify(response)



@routes.route('/adddamagedproduct',methods = ["POST","GET"])
def adddamagedproduct():
    manufacturer_name = str(request.json.get("manufacturer"))
    product_name = str(request.json.get("productname"))
    quantity = str(request.json.get("quantity"))
    message = str(request.json.get("message"))
    today = date.today()
    dateT = today.strftime("%b-%d-%Y")
    sql = "INSERT INTO damages VALUES(0,%s,%s,%s,%s,%s)"

    reponse = db.insertDataToTable(sql,manufacturer_name,product_name,quantity,message,dateT)

    if reponse:
        return jsonify({"response":"successful added product","code":200})
    else:
        return jsonify({"response":"failed to add product","code":300})

@routes.route('/getdamagedproducts',methods = ["POST","GET"])
def getdamagedproducts():
    response = db.selectAllFromtables(tb.selectdamaged)

    return jsonify(response)
    
