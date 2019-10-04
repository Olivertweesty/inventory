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

	sql = "INSERT INTO employees VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	reponse = db.insertDataToTable(sql,firstname,middlename,lastname,identification_number,identification,expiryD,kra_pin,huduma_number,email,mobile1,mobile2,residence,designation,department,next_of_kin,relatioship,n_tel_num1,n_tel_num2)
	sqlID = "SELECT MAX(id) FROM employees"

	responseISD = db.selectAllFromtables(sqlID)

	employeeid = responseISD[0]['MAX(id)']
	sql2 = "INSERT INTO leaveDays VALUES(0,%s,'0','0')"
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