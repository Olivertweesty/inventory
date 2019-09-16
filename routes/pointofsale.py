from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request

db = Database("inventorymanagementsystem","9993revilo")

@routes.route('/pointofsale')
def pointofsale():
    return render_template("pos_main.html")

@routes.route('/getposproducts',methods = ["POST","GET"])
def getposproducts():
    response = db.selectAllFromtables(tb.selectproductPOS)

    return jsonify(response)