#! /usr/bin/env python3
# coding: utf-8

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import source.model.classtable as ctable
import source.model.requestoff as roff
import source.constant as constant


class Dbase:

    def __init__(self):

        self.engine = create_engine(constant.ENGINE)
        self.engine.execute("DROP DATABASE IF EXISTS " + constant.DBASE)
        self.engine.execute("CREATE DATABASE " + constant.DBASE)
        self.engine.execute("USE " + constant.DBASE)

        Base = declarative_base()
        ctable.Base.metadata.create_all(bind=self.engine)

    def filldb(self):

        pref = {'categories weight': roff.Request.categories_by_number()}
        products = roff.Request().getproducts(pref)

        for product in products:
            self.insertProduct(product)

    def insertProduct(self, productdict):
        Session = sessionmaker(bind=self.engine)

        session = Session()

        nova = {1: ctable.Nova.one,
                2: ctable.Nova.two,
                3: ctable.Nova.three,
                4: ctable.Nova.four,
                10: ctable.Nova.unknown}
        nutriscore = {'A': ctable.NutriScore.A,
                      'B': ctable.NutriScore.B,
                      'C': ctable.NutriScore.C,
                      'D': ctable.NutriScore.D,
                      'E': ctable.NutriScore.E,
                      'UK': ctable.NutriScore.unknown,}

        product = ctable.Product()
        product.product_id = 0
        product.product_name = productdict['product_name'][:50] if 'product_name' in productdict else 'unknown'
        product.brand = productdict['brands'][:50]
        attr = int(productdict['nova_group'])\
            if 'nova_group' in productdict else 10
        product.nova = nova[attr]
        attr = productdict['nutriscore_grade'].upper()\
            if 'nutriscore_grade' in productdict else 'UK'
        product.nutriscore = nutriscore[attr]
        product.ingredient = {}

        session.add(product)
        session.commit()

        session.close()
