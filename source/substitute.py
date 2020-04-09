from sqlalchemy import create_engine
from sqlalchemy.sql import select

import source.constant as constant
import source.model as model

engine = create_engine(constant.ENGINE)
engine.execute("USE " + constant.DBASE)

def findSubstitute(product_id):

    s = select([model.ProductCategories.category_id]).where(model.ProductCategories.product_id == product_id)
    categories = tuple(c[0] for c in engine.execute(s))
    count = len(categories)

    s = "SELECT product_id, COUNT(*) FROM product_categories WHERE category_id IN " \
        + str(categories) \
        + "AND product_id != {}".format(product_id) \
        + " GROUP BY product_id"

    products = [prod[0] for prod in engine.execute(s) if prod[1] == count]

    return products

def valSubstitute(products):
    s = select([model.Product]).where(model.Product.product_id.in_(products))
    products = engine.execute(s).fetchall()
    productsval = [(product, value(product)) for product in products]

    return products

def value(product):

    coef = constant.PREF['value weight']

    nova = {model.Nova.one: 4,
            model.Nova.two: 3,
            model.Nova.three: 2,
            model.Nova.four: 1,
            model.Nova.unknown: 0}
    nutriscore = {model.NutriScore.A: 5,
                  model.NutriScore.B: 4,
                  model.NutriScore.C: 3,
                  model.NutriScore.D: 2,
                  model.NutriScore.E: 1,
                  model.NutriScore.unknown: 0}

    # NOVA goes from 1 to 4, 1 being the best.
    # (20 * 4 = 60 so it goes from 60 to 0)
    value = nova[product.nova] * 20 \
        * coef['nova']

    # Nutriscore goes from A to E, A being the best.
    # (12 * 5 = 60 so it goes from 60 to 0)
    value += nutriscore[product.nutriscore] * 12 \
        * coef['nutriscore']

    #value += (60 - min([origin.weight for origin in self.origins])) \
    #    * coef['origins']

    s = "SELECT * FROM label JOIN product_labels ON label.label_id = product_labels.label_id WHERE product_labels.product_id = {};".format(product.product_id)

    labels = engine.execute(s).fetchall()
    for label in labels:
        value += label.weight * coef['labels']

    return value

valSubstitute(findSubstitute(2))
