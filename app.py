from routes import *
from flask import Flask, request, url_for
from flask import render_template,redirect
from utils.Database import Database
import os
from flask import send_from_directory




app = Flask(__name__)
app.register_blueprint(routes)
db = Database("inventorymanagementsystem","9993revilo")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route("/login",methods=["GET","POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("pass")
    service = request.form.get("service")
    values = db.selectSpecificItemsFromDb("users","AND",username = username,password = password)
    if len(values) == 0:
        return redirect(url_for("main",message = "User Not Registered On A System"))
    elif service not in values[0]["access_rights"].split(","):
        return redirect(url_for("main",message = "User Does Not Have Rights to access {}".format(service)))
    else:
        if service == "warehouse":
            return redirect(url_for("routes.warehouse"))
        elif service == "pointofsale":
            return redirect(url_for("routes.pointofsale"))
        elif service == "accounting":
            return redirect(url_for("routes.account"))
        elif service == "humanresource":
            return redirect(url_for("routes.humanresource"))
        elif service == "admin":
            return redirect(url_for("routes.management"))
        else:
            return str(values)

@app.route("/",methods=["GET","POST"])
def main():
    return render_template("index.html")

@app.route("/login.html",methods=["GET","POST"])
def logout():
    return redirect(url_for("main"))

@app.route('/<name>')
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
    elif name == "missing":
        return render_template("hr_missing.html")
    elif name == "cash":
        return render_template("pos_cash_payment.html")
    elif name == "head_expenses":
        return render_template("head_expenses.html")
    elif name == "posPayments":
        return render_template("pos_payment.html")
    elif name == "served_orders":
        return render_template("warehouse_served_orders.html")
    elif name == "stocktaking":
        return render_template("warehouse_stocktaking.html")
    elif name == "dailyreport":
        return render_template("head_sales_report_daily.html")
    elif name == "monthlyreport":
        return render_template("head_sales_report_monthly.html")
    elif name == "manageusers":
        return render_template("head_manage_users.html")
    elif name == "posorders":
        return render_template("pos_order.html")
    elif name == "warehousetransactions":
        return render_template("warehouse_transactions.html")
    elif name == "head_all_products":
        return render_template("head_allproducts.html")
    elif name == "head_damaged":
        return render_template("head_damaged_products.html")
    elif name == "head_pending_orders":
        return render_template("head_pending_order.html")
    elif name == "head_served_orders":
        return render_template("head_served_order.html")
    elif name == "receipt":
        return render_template("receipt.html")
    elif name == "invoiceserved":
        return render_template("account_invoices.html")
    elif name == "invoicespending":
        return render_template("account_invoicespending.html")
    elif name == "expenses":
        return render_template("account_expenses.html")
    elif name == "payments":
        return render_template("account_payments.html")
    elif name == "dailyexpense":
        return render_template("account_daily_expense.html")
    elif name == "monthlyexpense":
        return render_template("account_monthly_expense.html")
    elif name == "monthlysales":
        return render_template("account_monthly_sales.html")
    elif name == "dailysales":
        return render_template("account_daily_sales.html")
    elif name == "employees":
        return render_template("hr_employees.html")
    elif name == "add_employee":
        return render_template("hr_add_employee.html")
    elif name == "leave":
        return render_template("hr_leave.html")
    elif name == "advancesalary":
        return render_template("hr_advance.html")
    elif name == "payslip":
        return render_template("hr_payslip.html")
    elif name == "payslipPrint":
        return render_template("payslip.html")
    else:
        return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True,port=4000,host="0.0.0.0")
    

