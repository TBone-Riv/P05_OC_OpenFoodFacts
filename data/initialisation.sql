DROP TABLE IF EXISTS Product_Association;
DROP TABLE IF EXISTS Product_Categories;
DROP TABLE IF EXISTS Product_Labels;
DROP TABLE IF EXISTS Product_Origins;
DROP TABLE IF EXISTS Product_Stores;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Label;
DROP TABLE IF EXISTS Store;
DROP TABLE IF EXISTS Origin;
DROP TABLE IF EXISTS Product;

CREATE TABLE Category (
  category_id int,
  category_name varchar(50),
  PRIMARY KEY (category_id)
);

CREATE TABLE Label (
  label_id int,
  label_name varchar(50),
  Weight int,
  PRIMARY KEY (label_id)
);

CREATE TABLE Store (
  store_id int,
  store_name varchar(50),
  PRIMARY KEY (store_id)
);

CREATE TABLE Origin (
  origin_id int,
  origin_name varchar(50),
  weight int,
  PRIMARY KEY (origin_id)
);

CREATE TABLE Product (
  product_id int,
  product_name varchar(50),
  brand varchar(50),
  nova enum('1', '2', '3', '4'),
  nutri_score enum('A','B','C','D','E'),
  PRIMARY KEY (product_id)
);

CREATE TABLE Product_Categories (
  product_id int,
  category_id int,
  PRIMARY KEY (product_id, category_id),
  FOREIGN KEY (product_id) REFERENCES Product(product_id),
  FOREIGN KEY (category_id) REFERENCES Category(category_id)
);

CREATE TABLE Product_Association (
  product_id int,
  association_id int,
  PRIMARY KEY (product_id, association_id),
  FOREIGN KEY (association_id) REFERENCES Product(product_id)
);

CREATE TABLE Product_Labels (
  product_id int,
  label_id int,
  PRIMARY KEY (product_id, label_id),
  FOREIGN KEY (product_id) REFERENCES Product(product_id),
  FOREIGN KEY (label_id) REFERENCES Label(label_id)
);

CREATE TABLE Product_Origins (
  product_id int,
  origin_id int,
  PRIMARY KEY (product_id, origin_id),
  FOREIGN KEY (product_id) REFERENCES Product(product_id),
  FOREIGN KEY (origin_id) REFERENCES Origin(origin_id)
);

CREATE TABLE Product_Stores (
  product_id int,
  store_id int,
  PRIMARY KEY (product_id, store_id),
  FOREIGN KEY (product_id) REFERENCES Product(product_id),
  FOREIGN KEY (store_id) REFERENCES Store(store_id)
);


