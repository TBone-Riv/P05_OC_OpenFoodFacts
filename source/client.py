#! /usr/bin/env python3
# coding: utf-8
"""Make use of library requests.py to get the list of products from Open Food Fact"""

from requests import get


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
                  "page_size": seize if seize != 1 else 2,
                  "json": 1}

        res = get(url, params=params)

        if res.status_code != 200:
            raise ConnectionError()

        products = res.json()["products"]
        return products if seize != 1 else products[:1]

    def getproducts(self, pref):
        """Retrieve products based on category weight"""

        categories_weight = pref['categories weight']

        allproducts = []

        for category in categories_weight:
            res = self.searchrequest(category, categories_weight[category])
            allproducts.extend(res)
        return allproducts

    @staticmethod
    def categories():
        """ Return categories with weight depend on the number of products """

        url = 'https://fr.openfoodfacts.org/categories.json'

        res = get(url)

        if res.status_code != 200:
            raise ConnectionError()

        categories = {category['id']: category['products']
                      for category in res.json()['tags']}

        return categories

    @staticmethod
    def label():
        """ Return categories with weight depend on the number of products """

        url = 'https://fr.openfoodfacts.org/labels.json'

        res = get(url)

        if res.status_code != 200:
            raise ConnectionError()

        labels = {category['id']: category['products']
                  for category in res.json()['tags']}

        return labels
