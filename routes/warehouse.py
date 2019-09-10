from flask import render_template
from . import routes

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