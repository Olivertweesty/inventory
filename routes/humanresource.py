from flask import render_template
from . import routes
from utils.Database import Database
import utils.tables as tb
from flask import jsonify
from flask import request
import json
from datetime import datetime

db = Database("inventorymanagementsystem","9993revilo")

@routes.route("/addemployee",methods=['POST'])
def addemployees():
	firstname = str(request.json.get("firstname"))
	basicpay = str(request.json.get("basicpay"))
	nssf = str(request.json.get("nssf"))
	nhif = str(request.json.get("nhif"))
	employeeid = str(request.json.get("employeeID"))
	middlename = str(request.json.get("middlename"))
	lastname = str(request.json.get("lastname"))
	identification = str(request.json.get("identification"))
	identification_number = str(request.json.get("identification_number"))
	expiryD = str(request.json.get("expiryD"))
	kra_pin = str(request.json.get("kra_pin"))
	huduma_number = str(request.json.get("huduma_number"))
	email = str(request.json.get("email"))
	mobile1 = str(request.json.get("mobile1"))
	mobile2 = str(request.json.get("mobile2"))
	residence = str(request.json.get("residence"))
	designation = str(request.json.get("designation"))
	department = str(request.json.get("department"))
	relatioship = str(request.json.get("relatioship"))
	n_tel_num2 = str(request.json.get("n_tel_num2"))
	n_tel_num1 = str(request.json.get("n_tel_num1"))
	next_of_kin = str(request.json.get("next_of_kin_name"))

	sql = "INSERT INTO employees VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	reponse = db.insertDataToTable(sql,firstname,middlename,lastname,basicpay,employeeid,nssf,nhif,identification_number,identification,expiryD,kra_pin,huduma_number,email,mobile1,mobile2,residence,designation,department,next_of_kin,relatioship,n_tel_num1,n_tel_num2)
	sqlID = "SELECT MAX(id) FROM employees"

	responseISD = db.selectAllFromtables(sqlID)

	employeeid = responseISD[0]['MAX(id)']
	sql2 = "INSERT INTO leaveDays VALUES(0,%s,'15')"
	db.insertDataToTable(sql2,employeeid)
	if reponse:
		return jsonify({"response":"successful added employee","code":200})
	else:
		return jsonify({"response":"failed to add employee","code":300})

@routes.route("/getemployees",methods=['GET'])
def getemployees():
	sql = "SELECT * FROM employees"
	response = db.selectAllFromtables(sql)
	return jsonify(response)

@routes.route("/getleaves/<id>",methods=['GET'])
def getleaves(id):
	sql = "SELECT * FROM leaveDays WHERE employeeID = '{}'".format(id)
	response = db.selectAllFromtables(sql)
	return jsonify(response)

@routes.route("/applyleave",methods=['POST'])
def applyleave():
	employeeID = str(request.json.get("employeeid"))
	startdate = str(request.json.get("startdate"))
	enddate = str(request.json.get("enddate"))
	days_sought = int(request.json.get("days_sought"))
	sql = "INSERT INTO leaveHistory VALUES(0,%s,%s,%s)"
	db.insertDataToTable(sql,employeeID,startdate,enddate)
	sql2 = "SELECT annual_leave FROM leaveDays WHERE employeeID = '{}'".format(employeeID)
	response = db.selectAllFromtables(sql2)
	days_due = int(response[0]['annual_leave']) - days_sought
	sql = "UPDATE leaveDays SET annual_leave='{}' WHERE id = '{}'".format(days_due,employeeID)
	response = db.updaterecords(sql)
	if response:
		return jsonify({"response":"Leave successful Applied","code":200})
	else:
		return jsonify({"response":"Leave Application Failed","code":300})

@routes.route("/generatepayslip/<id>", methods = ['POST','GET'])
def generatepayslip(id):
	sql = "SELECT * FROM employees WHERE id={}".format(id)
	response = db.selectAllFromtables(sql)
	dateTimeObj = datetime.now()
	dt = dateTimeObj.strftime("%d-%m-%Y")
	response = dict(response[0])
	response['date'] = dt
	response['housing'] = 0
	return jsonify(response)