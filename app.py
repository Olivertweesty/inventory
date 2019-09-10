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
        return redirect(url_for("main"))
    elif service not in values[0]["access_rights"].split(","):
        return redirect(url_for("main"))
    else:
        if service == "warehouse":
            return redirect(url_for("routes.warehouse"))
        elif service == "pointofsale":
            return redirect(url_for("routes.pointofsale"))
        else:
            return str(values)

@app.route("/",methods=["GET","POST"])
def main():
    db.insertDataToTable("products", "Watiti","Oliver")
    return render_template("index.html")

if __name__ == "__main__":
    try:
        app.run(debug=True,port=4000,host="127.0.0.1")
    except:
        app.run(debug=True,port=4000,host="0.0.0.0")

