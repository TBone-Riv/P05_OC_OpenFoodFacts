#! /usr/bin/env python3
# coding: utf-8
"""Make use of library requests.py to get the list of products from Open Food Fact"""

from requests import get

import source.constant as constant


class Request:
    """ Handle request to API OFF"""

    @staticmethod
    def searchrequest(category, seize):
        """Retrieve data of many products using a Search Requests"""

        url = "https://world.openfoodfacts.org/cgi/search.pl?"
        params = {"action": "process",
                  "tagtype_0": "purchase_places",
                  "tag_contains_0": "contains",
                  "tag_0": "france",
                  "tagtype_1": "categories",
                  "tag_contains_1": "contains",
                  "tag_1": category,
                  "sort_by": "unique_scans_n",
                  "page_size": seize,
                  "json": 1}

        res = get(url, params=params)

        if res.status_code != 200:
            raise ConnectionError()

        products = res.json()["products"]
        return products

    def getproducts(self, pref):
        """Retrieve products based on category weight"""

        categories_weight = pref['categories weight']

        allproducts = []

        for category, weight in categories_weight.item():
            allproducts += self.searchrequest(category, weight)

        return allproducts

    @staticmethod
    def categories_by_number():
        """ Return categories with weight depend on the number of products """

        url = 'https://world.openfoodfacts.org/categories.json'

        res = get(url)

        if res.status_code != 200:
            raise ConnectionError()

        categories_brut = {category['name']: category['products']
                           for category in res.json()['tags']}

        coef_sample = int(sum(categories_brut.values()) / constant.SEIZE_SAMPLE)

        categories_relative = {name: int(weight / coef_sample) for name, weight in categories_brut.items()}

        while sum(categories_relative.values()) < constant.SEIZE_SAMPLE:

            coef_sample += -10
            categories_relative = {name: int(weight / coef_sample) for name, weight in categories_brut.items()}

        categories = {}

        for name, weight in categories_relative.items():
            if weight != 0:
                categories[name] = weight

        return categories

    @staticmethod
    def categories_by_popularity():
        """ Return categories with weight depend on the number of times a
        category appears on the first page of the 100 popular product """

        url = "https://world.openfoodfacts.org/cgi/search.pl?"
        params = {"action": "process",
                  "sort_by": "unique_scans_n",
                  "page_size": 100,
                  "json": 1}

        res = get(url, params=params)

        if res.status_code != 200:
            raise ConnectionError()

        products = res.json()["products"]

        categories_brut = {}

        for product in products:
            for category in product['categories_tags']:
                if category not in categories_brut:
                    categories_brut[category] = 1
                else:
                    categories_brut[category] += 1

        coef_sample = int(sum(categories_brut.values()) / constant.SEIZE_SAMPLE) - 1

        categories_relative = {name: int(weight / coef_sample) for name, weight in categories_brut.items()}

        categories = {}

        for name, weight in categories_relative.items():
            if weight != 0:
                categories[name] = weight

        return categories


print(Request().categories_by_popularity())
