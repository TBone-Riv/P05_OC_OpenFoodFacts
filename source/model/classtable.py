#! /usr/bin/env python3
# coding: utf-8

import enum
from sqlalchemy import Column, Integer, String, Enum, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

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
    """ """
    __tablename__ = 'product'

    product_id = Column('product_id', Integer, primary_key=True)
    product_name = Column('name', String(50))
    brand = Column('brand', String(50))
    nova = Column('nova', Enum(Nova))
    nutriscore = Column('nutriscore', Enum(NutriScore))
    ingredient = Column('ingredient', JSON)

    def __init__(self):
        super().__init__()
        self.categories = []
        self.labels = []
        self.origins = []
        self.stores = []

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

    def value(self, pref):
        """ Calculate how "good" the product is taking
         the currant preference """

        coef = pref['value weight']

        # NOVA goes from 1 to 4, 1 being the best.
        # (20 * 4 = 60 so it goes from 60 to 0)
        value = (abs(self.nova - 4) * 20) \
            * coef['nova']

        # Nutriscore goes from A to E, A being the best.
        # (12 * 5 = 60 so it goes from 60 to 0)
        value += (['E', 'D', 'C', 'B', 'A'].index(self.nutriscore) * 12) \
            * coef['nutriscore']

        value += (60 - min([origin.weight for origin in self.origins])) \
            * coef['origins']

        for label in self.labels:
            value += label.weight * coef['labels']

        return value

    def similar(self, product):
        """ Compare the product with an other """


class Category:
    __tablename__ = 'category'
    category_id = Column('category_id', Integer, primary_key=True)
    category_name = Column('category_name', String(50))

    def isin(self, product: Product):
        return self.category_name in product.categories


class Label:
    __tablename__ = 'label'
    label_id = Column('category_id', Integer, primary_key=True)
    label_name = Column('category_name', String(50))
    weight = Column('weight', Integer)


class Origin:
    __tablename__ = 'origin'
    origin_id = Column('origin_id', Integer, primary_key=True)
    origin_name = Column('origin_name', String(50))
    weight = Column('weight', Integer)


class Store:
    __tablename__ = 'store'
    store_id = Column('store_id', Integer, primary_key=True)
    store_name = Column('store_name', String(50))


class ProductAssociation:
    __tablename__ = 'product_association'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    association_id = Column('association_id', Integer,
                            ForeignKey('product.product_id'), primary_key=True)


class ProductCategories:
    __tablename__ = 'product_categories'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    category_id = Column('category_id', Integer,
                         ForeignKey('category.category_id'), primary_key=True)


class ProductLabels:
    __tablename__ = 'product_labels'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    association_id = Column('label_id', Integer,
                            ForeignKey('label.label_id'), primary_key=True)


class ProductOrigins:
    __tablename__ = 'product_origins'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    association_id = Column('origin_id', Integer,
                            ForeignKey('origin.origin_id'), primary_key=True)


class ProductStores:
    __tablename__ = 'product_stores'
    product_id = Column('product_id', Integer,
                        ForeignKey('product.product_id'), primary_key=True)
    association_id = Column('store_id', Integer,
                            ForeignKey('store.store_id'), primary_key=True)
