from flask import render_template
from . import routes
from flask import jsonify
from flask import request
from utils.Database import Database

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
    else:
        return render_template("404.html")
@routes.route('/checkinproducts',methods = ["POST"])
def checkin_products():
    manufacterer = str(request.json.get("manufacterer"))
    productname = str(request.json.get("productname"))
    unit_of_measument = str(request.json.get("unit_of_measument"))
    quantity = str(request.json.get("quantity"))
    purchase_price = str(request.json.get("purchase_price"))

    return ""

@routes.route('/addproductname',methods = ["POST"])
def addproductname():
    product_name = str(request.json.get("productname"))
    
    sql = "INSERT INTO products_name VALUES(0,%s)"
    reponse = db.insertDataToTable(sql,product_name)
    print(reponse)
    if reponse:
        return jsonify({"response":"successful added product","code":200})
    else:
        return jsonify({"response":"failed to add product","code":300})

@routes.route('/getdatafromtable/<name>',methods = ["POST"])
def getdatafromtable(name):
    response = db.selectAllFromtables(name)

    if not response:
        return jsonify({"response":"failed to retrieve data","code":300})
    else:
        return jsonify({"response":response,"code":300})
    