from flask import render_template
from . import routes
from flask import jsonify
from flask import request
from utils.Database import Database
import utils.tables as tb
from datetime import date
from datetime import datetime
import json

db = Database("inventorymanagementsystem","9993revilo")

@routes.route('/warehouse')
def warehouse():
    return render_template("warehouse_dashboard.html")



def getSingleItemFromTable(table, **kwargs):
    key = list([key for key, value in kwargs.items()])
    key = key[0]
    value = [value for key, value in kwargs.items()]
    print(value)
    sql = "SELECT * FROM {} WHERE {} = '{}'".format(table,key,value[0])
    response = db.selectAllFromtables(sql)
    print(sql)
    return response

@routes.route("/summarywarehouse", methods = ['POST'])
def getSummary():
    return


@routes.route('/checkinproducts',methods = ["POST"])
def checkin_products():
    manufacterer = str(request.json.get("manufacterer"))

    manufacterer_name = getSingleItemFromTable("manufacterer",id=manufacterer)
    print(manufacterer_name)
    manufacterer_name = (manufacterer_name[0]['manufacterer']).upper()
    productname = str(request.json.get("productname"))
    product_name = getSingleItemFromTable("products_name",id=productname)
    product_name = (product_name[0]['product_name']).upper()
    quantity_alert = str(request.json.get("quantity_alert"))
    unit_of_measument = str(request.json.get("unit_of_measument"))
    quantity = str(request.json.get("quantity"))
    purchase_price = str(request.json.get("purchase_price"))
    selling_price = str(request.json.get("selling_price"))
    
    product_code = str(request.json.get("productcode"))
    # (manufacterer_name[0:4]+product_name[0:4])

    print(product_code)

    existance = db.selectSpecificItemsFromDb("products","AND",product_code=product_code,manufacturer=manufacterer,product_name=productname)
    if len(existance) == 0:
        sql = "INSERT INTO products VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        response = db.insertDataToTable(sql,product_code,manufacterer,productname,purchase_price,unit_of_measument,selling_price,"0",quantity,quantity_alert)
    else:
        new_quantity = int(existance[0]['quantity']) + int(quantity)
        sql = "UPDATE products SET quantity = %s WHERE product_code=%s AND manufacturer=%s AND product_name=%s AND selling_price = %s"
        response = db.insertDataToTable(sql,new_quantity,product_code,manufacterer,productname,selling_price)

    existance = db.selectSpecificItemsFromDb("products","AND",product_code=product_code,manufacturer=manufacterer,product_name=productname)
    product_id = existance[0]['id']
    today = date.today()
    dateT = today.strftime("%b-%d-%Y")
    sql2 = "INSERT INTO transactions VALUES(0,%s,%s,%s,'active')"
    response2 = db.insertDataToTable(sql2,product_id,quantity,dateT)

    if response == True:
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
        return jsonify({"response":"successful added Product Name","code":200})
    else:
        return jsonify({"response":"failed to add Manufacterer","code":300})



@routes.route('/addproductcode',methods = ["POST"])
def addproductcode():
    product_code = str(request.json.get("productcode"))
    
    sql = "INSERT INTO productCodes VALUES(0,%s)"
    reponse = db.insertDataToTable(sql,product_code)
    print(reponse)
    if reponse:
        return jsonify({"response":"successful added Product Code","code":200})
    else:
        return jsonify({"response":"failed to add Product Code","code":300})



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

@routes.route('/getallorders/<typeoforders>',methods = ["POST","GET"])
def getsingleorders(typeoforders):
    response = db.selectAllFromtables(tb.selectOrders.format(typeoforders))

    return jsonify(response)

def getItemNameByID(id):
    sql = tb.selectProductnameById.format(id)
    response = db.selectAllFromtables(sql)
    return response[0]


@routes.route('/getsingleorder/<id>',methods = ["POST","GET"])
def getallorders(id):
    sql = "SELECT orderid,items,date_served,date FROM orders WHERE id = '{}'".format(id)
    response = db.selectAllFromtables(sql)
    ids = dict(response[0])['items']
    ids = json.loads(ids.replace("'",'"'))
    response = {"orderid" : dict(response[0])['orderid'],"date":dict(response[0])['date'],"date_served": dict(response[0])['date_served'], "items":[]}
    for id_ in ids:
        itemName = getItemNameByID(id_['item'])
        itemName['quantity'] = id_['quantity']
        itemName['discount'] = id_['discount']
        response['items'].append(itemName) 
    

    return jsonify(response)

@routes.route('/getreciept/<id>',methods = ["POST","GET"])
def getreciept(id):
    sql = "SELECT o.orderid,o.items,o.date_served,o.date,c.mobile_number,o.tax,o.total_paid,o.payment_type,o.transport,o.discount,c.name,c.company_name FROM orders as o JOIN customers as c ON c.id = o.customer_id WHERE o.id = '{}'".format(id)
    response = db.selectAllFromtables(sql)
    ids = dict(response[0])['items']
    ids = json.loads(ids.replace("'",'"'))
    print(response)
    response = {"orderid" : dict(response[0])['orderid'],
                "payment_type":dict(response[0])['payment_type'],
                "total_paid":dict(response[0])['total_paid'],
                "date":dict(response[0])['date'],
                "customer_name" : dict(response[0])['name'],
                "company_name": dict(response[0])['company_name'],
                "mobile_number" : dict(response[0])['mobile_number'],
                "transport": dict(response[0])['transport'],
                "tax": dict(response[0])['tax'],
                "discount" : dict(response[0])['discount'],
                "date_served": dict(response[0])['date_served'], 
                "items":[]}
    for id_ in ids:
        itemName = getItemNameByID(id_['item'])
        itemName['quantity'] = id_['quantity']
        itemName['product_code'] = id_['prod_code']
        itemName['discount'] = id_['discount']
        response['items'].append(itemName)

    

    return jsonify(response)

@routes.route('/processOrder/<id>',methods = ["POST","GET"])
def processOrder(id):
    sql = "SELECT orderid FROM orders WHERE id = '{}'".format(id)
    response = db.selectAllFromtables(sql)
    
    orderid = response[0]['orderid']

    sql2 = "UPDATE orders SET checkout_status='served' WHERE orderid = '{}'".format(orderid)
    response = db.updaterecords(sql2)

    if response:
        return jsonify({"response":"successful processed order","code":200})
    else:
        return jsonify({"response":"failed to process order","code":300})


@routes.route('/gettransactions',methods = ["POST","GET"])
def gettransactions():
    response = db.selectAllFromtables(tb.selectTransactions)
    response2 = []
    for transaction in response:
        data = {}
        data['id'] = transaction['id']
        data['product_name'] = getSingleItemFromTable("products_name",id=transaction['product_name'])[0]['product_name']
        data['manufacturer'] = getSingleItemFromTable("manufacterer",id=transaction['manufacturer'])[0]['manufacterer']
        data['date'] = transaction['date']
        data['status'] = transaction['status']
        data['quantity'] = transaction['quantity']
        response2.append(data)
    return jsonify(response2)




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
    sql = "SELECT quantity FROM products WHERE product_name = '{}' AND manufacturer = '{}'".format(product_name,manufacturer_name)
    dquantity = ""
    try:
        dquantity = db.selectAllFromtables(sql)[0]['quantity']
        dquantity = int(dquantity) - int(quantity)
        sql = "UPDATE products SET quantity = '{}' WHERE id = '{}'".format(dquantity,product_name)
        db.updaterecords(sql)
        if reponse:
            return jsonify({"response":"successful added product","code":200})
        else:
            return jsonify({"response":"failed to add product","code":300})
    except Exception as e:
        return jsonify({"response":"Product Does Not Exist","code":200})
    

@routes.route('/getdamagedproducts',methods = ["POST","GET"])
def getdamagedproducts():
    response = db.selectAllFromtables(tb.selectdamaged)

    return jsonify(response)

@routes.route('/reversetransaction/<id>',methods = ["POST","GET"])
def reversetransaction(id):
    sql = "SELECT product_id,quantity FROM transactions WHERE id='{}'".format(id)
    response = db.selectAllFromtables(sql)
    product_id = response[0]['product_id']
    quantity = response[0]['quantity']

    sql2 = "SELECT quantity FROM products WHERE id = '{}'".format(product_id)
    response2 = db.selectAllFromtables(sql2)
    quantity_2 = response2[0]['quantity']

    new_quantity = quantity_2 - quantity
    if new_quantity < 0:
        return jsonify({"response":"Unable to reverse transaction Because Some quantity have been used"})
    else:
        sql3 = "UPDATE products SET quantity={} WHERE id={}".format(new_quantity,product_id)
        response = db.updaterecords(sql3)
        if response:
            return jsonify({"response":"Reversal successful"})
        else:
            return jsonify({"response":"Unable to reverse transaction"})

    return jsonify(new_quantity)

@routes.route('/warehousemain', methods = ['POST','GET'])
def warehousemain():
    response = {}
    sql = "SELECT * FROM products"
    products = db.selectAllFromtables(sql)
    outofstock = 0
    sql = "SELECT SUM(quantity) AS quantity FROM damages"
    damages = db.selectAllFromtables(sql)
    total_selling_price = 0
    for product in products:
        total_selling_price = total_selling_price + (float(product['selling_price']) * int(product['quantity']))
        if int(product['quantity_alert'] > int(product['quantity'])):
            outofstock = outofstock + 1
    sql = "SELECT * FROM orders"
    orders = db.selectAllFromtables(sql)
    data_to_return = []
    for order in orders:
        order_date = datetime.strptime(order['date'],"%b-%d-%Y %H:%M:%S")
        if order_date.date() == datetime.now().date():
            data_to_return.append(order)
    
    response['stock'] = total_selling_price
    response['orders'] = str(len(data_to_return))
    response['damages'] = str(damages[0]['quantity'])
    response['outofstock'] = outofstock
    response['products_available'] = len(products)
    return jsonify(response)

    
