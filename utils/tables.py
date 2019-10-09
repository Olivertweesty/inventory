appusers = """CREATE TABLE IF NOT EXISTS users(
                                    `id` int(11) AUTO_INCREMENT,
                                    `userid` varchar(70) NOT NULL,
                                    `username` varchar(20) NOT NULL,
                                    `access_rights` varchar(300) NOT NULL,
                                    `phone` varchar(20),
                                    `password` varchar(20),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

transactions = """CREATE TABLE IF NOT EXISTS transactions(
                                    `id` int(11) AUTO_INCREMENT,
                                    `product_id` int(11) NOT NULL,
                                    `quantity` int(20) NOT NULL DEFAULT 0,
                                    `date` VARCHAR(20) NOT NULL,
                                    `status` VARCHAR(20) NOT NULL,
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

products = """CREATE TABLE IF NOT EXISTS products(
                                    `id` int(11) AUTO_INCREMENT,
                                    `product_code` varchar(200) NOT NULL UNIQUE,
                                    `manufacturer` varchar(170) NOT NULL,
                                    `product_name` varchar(200) NOT NULL,
                                    `purchase_price` varchar(200) NOT NULL DEFAULT '0',
                                    `unit_of_measurment` varchar(20),
                                    `selling_price` varchar(200) DEFAULT '0',
                                    `quantity` int(200) DEFAULT 0,
                                    `quantity_alert` int(200) DEFAULT 0,
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

product_names = """CREATE TABLE IF NOT EXISTS products_name(
                                    `id` int(11) AUTO_INCREMENT,
                                    `product_name` varchar(200) NOT NULL,
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

manufacterer = """CREATE TABLE IF NOT EXISTS manufacterer(
                                    `id` int(11) AUTO_INCREMENT,
                                    `manufacterer` varchar(200) NOT NULL UNIQUE,
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

damages = """CREATE TABLE IF NOT EXISTS damages(
                                    `id` int(11) AUTO_INCREMENT,
                                    `manufacterer_id` varchar(200) NOT NULL,
                                    `product_id` varchar(200) NOT NULL,
                                    `quantity` int(20) DEFAULT '0',
                                    `message` varchar(1000),
                                    `date` varchar(200),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

orders = """CREATE TABLE IF NOT EXISTS orders(
                                    `id` int(20) AUTO_INCREMENT,
                                    `orderid` varchar(40) NOT NULL,
                                    `items` varchar(2000) NOT NULL,
                                    `date` varchar(20),
                                    `customer_id` varchar(20),
                                    `transport` varchar(20) DEFAULT '0',
                                    `discount` varchar(20) DEFAULT '0',
                                    `checkout_status` varchar(20),
                                    `payment_status` varchar(20),
                                    `total_amount` varchar(200) DEFAULT '0',
                                    `total_paid` varchar(200) DEFAULT  '0',
                                    `serve_status` varchar(20),
                                    `payment_type` varchar(20),
                                    `date_served` varchar(20),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""


payments = """CREATE TABLE IF NOT EXISTS payments(
                                    `id` int(20) AUTO_INCREMENT,
                                    `invoice_id` varchar(40) NOT NULL,
                                    `amount` varchar(40) NOT NULL DEFAULT '0',
                                    `customer_id` varchar(50) NOT NULL,
                                    `payment_type` varchar(40) NOT NULL,
                                    `date_paid` varchar(40) NOT NULL,
                                    `date_confirmed` varchar(40),
                                    `served_by` varchar(40) NOT NULL,
                                    `details` varchar(2000),
                                    `confirmed` varchar(30),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

customers = """CREATE TABLE IF NOT EXISTS customers(
                                    `id` int(20) AUTO_INCREMENT,
                                    `name` varchar(50) NOT NULL,
                                    `company_name` varchar(50),
                                    `mobile_number` varchar(20),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""
expenses = """CREATE TABLE IF NOT EXISTS expenses(
                                    `id` int(20) AUTO_INCREMENT,
                                    `date` varchar(50) NOT NULL,
                                    `use` varchar(2000) NOT NULL,
                                    `amount` varchar(50) NOT NULL DEFAULT '0',
                                    `type` varchar(20) NOT NULL,
                                    `status` varchar(50) NOT NULL,
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

employees = """CREATE TABLE IF NOT EXISTS employees(
                                    `id` int(20) AUTO_INCREMENT,
                                    `firstname` varchar(20) NOT NULL,
                                    `middlename` varchar(20) NOT NULL,
                                    `lastname` varchar(20) NOT NULL,
                                    `basic_pay` varchar(20) NOT NULL DEFAULT '0',
                                    `employee_id` varchar(20) NOT NULL,
                                    `nssf` varchar(20) NOT NULL,
                                    `nhif` varchar(20) NOT NULL,
                                    `id_number` varchar(10),
                                    `identification` varchar(20),
                                    `expirydate` varchar(20),
                                    `kra_pin` varchar(20) NOT NULL,
                                    `hudumanumber` varchar(20),
                                    `email` varchar(30),
                                    `mobile1` varchar(20) NOT NULL,
                                    `mobile2` varchar(20),
                                    `residence` varchar(50),
                                    `designation` varchar(20),
                                    `department` varchar(20),
                                    `next_name` varchar(50),
                                    `relationship` varchar(20),
                                    `next_number1` varchar(20),
                                    `next_number2` varchar(20),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""


leave = """CREATE TABLE IF NOT EXISTS leaveDays(
                                    `id` int(20) AUTO_INCREMENT,
                                    `employeeID` int(20),
                                    `annual_leave` varchar(10),
                                    `maternity_leave` varchar(10),
                                    `paternity_leave` varchar(10),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

leaveHist = """CREATE TABLE IF NOT EXISTS leaveHistory(
                                    `id` int(20) AUTO_INCREMENT,
                                    `employeeID` int(20),
                                    `startdate` varchar(20),
                                    `enddate` varchar(20),
                                    `type` varchar(20),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""



misseddays = """CREATE TABLE IF NOT EXISTS missingdays(
                                    `id` int(20) AUTO_INCREMENT,
                                    `employeeID` int(20),
                                    `startdate` varchar(20) DEFAULT '0',
                                    `enddate` varchar(20) DEFAULT '0',
                                    `number_of_days` varchar(20) DEFAULT '0',
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""



advance = """CREATE TABLE IF NOT EXISTS advance(
                                    `id` int(20) AUTO_INCREMENT,
                                    `employeeID` int(20),
                                    `amount` varchar(20),
                                    `cashout` varchar(20),
                                    `status` varchar(20),
                                    `date_given` varchar(20),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""
selectallproduct = """SELECT p.id, product_code,n.product_name, quantity,
                            m.manufacterer FROM products 
                            AS p JOIN products_name 
                            AS n JOIN manufacterer as m WHERE p.product_name = n.id AND m.id = p.manufacturer"""


selectproductPOS = """SELECT ap.id,m.manufacterer,p.product_name, ap.selling_price,ap.quantity FROM products AS ap JOIN manufacterer AS m JOIN products_name AS p WHERE p.id = ap.product_name AND m.id = ap.manufacturer"""
selectdamaged = """SELECT m.manufacterer,p.product_name,d.quantity,d.date FROM damages AS d JOIN manufacterer AS m JOIN products_name AS p WHERE p.id = d.product_id AND m.id = d.manufacterer_id"""

selectOrders = "SELECT o.id, o.orderid, o.date, c.name FROM orders as o JOIN customers as c WHERE c.id = o.customer_id AND o.checkout_status = '{}'"
selectProductnameById = "SELECT p.product_name, n.selling_price FROM products AS n JOIN products_name AS p WHERE n.product_name = p.id AND n.id ='{}'"
selectAllOrders = "SELECT o.id, o.orderid, o.date, c.name,o.checkout_status,o.payment_status,o.total_amount FROM orders as o JOIN customers as c WHERE c.id = o.customer_id"
selectTransactions = "SELECT t.*,p.product_name,p.manufacturer FROM transactions AS t JOIN products AS p WHERE t.product_id = p.id"
selectAllAccountsOrders = "SELECT o.id, o.orderid, o.date, c.name,o.checkout_status,o.payment_status,o.total_amount FROM orders as o JOIN customers as c WHERE c.id = o.customer_id AND o.serve_status = '{}'"