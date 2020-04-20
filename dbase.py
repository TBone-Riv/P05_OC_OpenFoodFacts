#! /usr/bin/env python3
# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, update

import source.client as client
import source.constant as constant
import source.model as model


class Dbase:

    def __init__(self):

        self.engine = create_engine(constant.ENGINE, encoding='utf-8')
        self.engine.execute("DROP DATABASE IF EXISTS " + constant.DBASE)
        self.engine.execute("CREATE DATABASE " + constant.DBASE)
        self.engine.execute("USE " + constant.DBASE)

        Base = declarative_base()

        # create table
        model.Base.metadata.create_all(bind=self.engine)

    def fill_dbase(self):
        """ Fill data base """

        # fill table 'category'
        # self.fill_category()

        pref = constant.PREF

        # get products
        products = client.Request().get_products()

        # fill table 'product'
        for product in products:
            self.insert_product(product)

    def fill_category(self):
        """ Fill table category """

        # get categories
        categories = client.Request().categories()

        # insert category
        for category, weight in categories.items():
            self.insert_category(category, weight)

    def insert_product(self, productdict):
        """ Insert product in product table """

        Session = sessionmaker(bind=self.engine)

        session = Session()

        name = productdict.get('generic_name', 'undefined name')
        brand = productdict.get('brands', '')
        nova = int(productdict.get('nova_group', 10))
        nutriscore = productdict.get('nutriscore_grade', 'UK').upper()
        categories = productdict.get('categories_tags', [])
        labels = productdict.get('labels_tags', [])
        stores = productdict.get('stores', '')

        # create product instance
        product = model.Product(
            name=name,
            brand=brand,
            nova=nova,
            nutriscore=nutriscore,
            categories=[i.encode("utf-8") for i in categories],
            labels=[i.encode("utf-8") for i in labels],
            origins=[],
            stores=stores
        )

        # not added if name not unique
        try:
            session.add(product)
            session.commit()
            returnval = 1
        except:
            returnval = 0

        # get id for relation table
        product_id = product.product_id
        session.close()

        if returnval:

            # fill category table if category not in, fill relation table
            for category in product.categories:

                # SELECT to check if category is in the table
                query = select([model.Category]).\
                    where(model.Category.category_id == category)
                row = [i for i in self.engine.execute(query)]

                # if not in we insert it
                if not row:
                    self.insert_category(category, 1)

                # insert in many to many relation table
                self.relation_categoty(product_id, category)

            # fill label table if label not in, fill relation table
            for label in product.labels:

                # SELECT to check if label is in the table
                query = select([model.Label]).\
                    where(model.Label.label_id == label)
                row = [i for i in self.engine.execute(query)]

                # if not in we insert it
                if not row:
                    self.insert_label(label, 1)

                # insert in many to many relation table
                self.relation_label(product_id, label)

            # update label score
            product.LabelScore()
            query = update(model.Product).\
                where(model.Product.product_id == product_id).\
                values(labelscore=product.labelscore)
            self.engine.execute(query)

    def insert_category(self, category_id, weight):
        """ Insert category in category table """

        Session = sessionmaker(bind=self.engine)

        session = Session()

        category = model.Category()
        category.category_id = category_id

        category.weight = weight

        session.add(category)
        session.commit()

        session.close()

    def relation_categoty(self, product_id, category_id):
        Session = sessionmaker(bind=self.engine)

        session = Session()

        relation = model.ProductCategories()
        relation.product_id = product_id
        relation.category_id = category_id

        session.add(relation)
        session.commit()

        session.close()

    def insert_label(self, label_id, weight):
        Session = sessionmaker(bind=self.engine)

        session = Session()

        label = model.Label()
        label.label_id = label_id
        label.label_name = label_id
        label.weight = weight

        session.add(label)
        session.commit()

        session.close()

    def relation_label(self, product_id, label_id):
        Session = sessionmaker(bind=self.engine)

        session = Session()

        relation = model.ProductLabels()
        relation.product_id = product_id
        relation.label_id = label_id

        try:
            session.add(relation)
            session.commit()
        except:
            pass

        session.close()


if __name__ == '__main__':
    Dbase().fill_dbase()
