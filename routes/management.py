from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request

db = Database("inventorymanagementsystem","9993revilo")

@routes.route('/management')
def management():
    return render_template("head_dashboard.html")

@routes.route("/getdailyreport", methods = ["POST","GET"])
def getdailyreport():
    return
