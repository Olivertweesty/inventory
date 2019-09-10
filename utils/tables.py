appusers = """CREATE TABLE IF NOT EXISTS users(
                                    `id` int(11) AUTO_INCREMENT,
                                    `name` varchar(200) NOT NULL,
                                    `email` varchar(70) NOT NULL,
                                    `username` varchar(20) NOT NULL,
                                    `access_rights` varchar(300) NOT NULL,
                                    `phone` varchar(20),
                                    `gender` varchar(20),
                                    `password` varchar(20),
                                    PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;"""

products = """CREATE TABLE IF NOT EXISTS products(
                                    `id` int(11) AUTO_INCREMENT,
                                    `product_id` varchar(200) NOT NULL UNIQUE,
                                    `manufacturer` varchar(170) NOT NULL,
                                    `product_name` varchar(200) NOT NULL,
                                    `purchase_price` varchar(200) NOT NULL,
                                    `unit_of_measurment` varchar(20),
                                    `selling_price` varchar(200),
                                    `quantity` varchar(200),
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

