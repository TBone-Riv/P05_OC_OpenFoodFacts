#! /usr/bin/env python3
# coding: utf-8

import enum

from sqlalchemy import Column, Integer, String, Enum, JSON, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, text

import source.constant as constant

Base = declarative_base()


class Nova(enum.Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    unknown = 10


class NutriScore(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    unknown = 'UK'


class Product(Base):
    """ Product """

    __tablename__ = 'product'

    product_id = Column('product_id', Integer, primary_key=True)
    product_name = Column('name', String(500), unique=True)
    brand = Column('brand', String(500))
    nova = Column('nova', Integer)
    nutriscore = Column('nutriscore', Enum(NutriScore))
    labelscore = Column('labelscore', Integer)
    ingredient = Column('ingredient', JSON)
    stores = Column('stores', String(500))

    def __init__(self, name, brand='', nova=10, nutriscore='UK', ingredient={},
                 categories=[], labels=[], origins=[], stores=''):

        super().__init__()

        self.product_name = name
        self.brand = brand
        self.nova = Nova(nova).value
        self.nutriscore = NutriScore(nutriscore)
        self.ingredient = ingredient

        self.categories = categories
        self.labels = labels
        self.origins = origins
        self.stores = stores

        self.labelscore = 0

    def __repr__(self):
        return {'id': self.product_id,
                'name': self.product_name,
                'brand': self.brand,
                'nova': self.nova,
                'nutriscore': self.nutriscore,
                'ingredient': self.ingredient,
                'categories': self.categories,
                'labels': self.labels,
                'origins': self.origins,
                'stores': self.stores
                }

    def __str__(self):
        return 'Produit {}, identifient : {}'.format(self.product_name,
                                                     self.product_id)

    def LabelScore(self):
        """ Update labelscore"""

        engine = create_engine(constant.ENGINE)
        engine.execute("USE " + constant.DBASE)

        for label in self.labels:
            query = select([Label.weight]).where(Label.label_id == label)
            val = [i for i in engine.execute(query)][0][0]

            self.labelscore += val


class Category(Base):
    __tablename__ = 'category'
    category_id = Column('category_id', String(500), primary_key=True)
    category_name = Column('category_name', String(500))
    weight = Column('weight', Integer)

    def isin(self, product: Product):
        return self.category_name in product.categories


class Label(Base):
    __tablename__ = 'label'
    label_id = Column('label_id', String(500), primary_key=True)
    label_name = Column('label_name', String(500))
    weight = Column('weight', Integer)


class Origin(Base):
    __tablename__ = 'origin'
    origin_id = Column('origin_id', Integer, primary_key=True)
    origin_name = Column('origin_name', String(500))
    weight = Column('weight', Integer)


class Store(Base):
    __tablename__ = 'store'
    store_id = Column('store_id', Integer, primary_key=True)
    store_name = Column('store_name', String(500))


class ProductAssociation(Base):
    __tablename__ = 'product_association'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    association_id = Column('association_id', Integer,
                            ForeignKey('product.product_id'), primary_key=True)


class ProductCategories(Base):
    __tablename__ = 'product_categories'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    category_id = Column('category_id', String(500),
                         ForeignKey('category.category_id'), primary_key=True)


class ProductLabels(Base):
    __tablename__ = 'product_labels'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    label_id = Column('label_id', String(500),
                      ForeignKey('label.label_id'), primary_key=True)


class ProductOrigins(Base):
    __tablename__ = 'product_origins'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    origin_id = Column('origin_id', Integer,
                       ForeignKey('origin.origin_id'), primary_key=True)


class ProductStores(Base):
    __tablename__ = 'product_stores'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    store_id = Column('store_id', Integer,
                      ForeignKey('store.store_id'), primary_key=True)


class RequestDBase:

    @staticmethod
    def get_products(page, engine, order=None,  search=None):
        """ Get products """

        index = 0 + 10 * (page - 1)

        query = "SELECT * FROM product"

        if search:
            query = query + " WHERE name LIKE {}".format("'%"+search+"%'")

        if order:
            query = query + " ORDER BY " + order

        query += " LIMIT {}, {}".format(index, 10)

        products = [i for i in engine.execute(text(query))]

        return products

    @staticmethod
    def get_similar(product_id, engine):
        """ Take a product id and return a list of 'similar' product """

        # get product categories
        query = select([ProductCategories.category_id]).\
            where(ProductCategories.product_id == product_id)
        categories = tuple(c[0] for c in engine.execute(query))

        # keep the number of category from the original for compareson
        count = len(categories)

        # get product w/ a category in list from original product
        # and count how many category it have in common
        query = "SELECT product_id, COUNT(*) AS nb_commune_category " \
                + "FROM product_categories " \
                + "WHERE category_id IN " + str(categories) \
                + "AND product_id != {} ".format(product_id) \
                + "GROUP BY product_id " \
                + "HAVING nb_commune_category = {} ".format(count)
        # keep product w/  x% category w/ x stock in pref

        products = tuple(prod[0] for prod in engine.execute(query))

        if products:
            query = "SELECT * FROM product WHERE product_id " \
                    + ("IN " + str(products) if len(products) > 1 else
                       "= {}".format(products[0])) \
                    + " ORDER BY " \
                    + ' ,'.join(constant.PREF['score weight'])
            # Last str sort product by value

            query += " LIMIT 5"

            products = [c for c in engine.execute(query)]
        else:
            products = []

        return products

    @staticmethod
    def get_save_substitute(page, engine, order=None):
        """ Get saved substitute """

        index = 0 + 10 * (page - 1)

        query = "SELECT product.name, association.name " + \
                "FROM product_association " \
                "JOIN product " + \
                "ON product.product_id = product_association.product_id " + \
                "JOIN product AS association " + \
                "ON association.product_id = " + \
                "product_association.association_id"

        if order:
            query = query + " ORDER BY " + order

        query = query + " LIMIT {}, {}".format(index, index + 10)

        substitutes = [i for i in engine.execute(query)]

        return substitutes


class OperationDBase:

    @staticmethod
    def save(product_id, association_id, engine):
        """ Save the selected association """

        Session = sessionmaker(bind=engine)

        session = Session()

        association = ProductAssociation()
        association.product_id = product_id
        association.association_id = association_id

        session.add(association)
        session.commit()

        session.close()
