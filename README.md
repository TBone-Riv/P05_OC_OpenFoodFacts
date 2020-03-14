# P05_OC_OpenFoodFacts
_Project 05 OpenClassrooms "Utilisez les données OpenFoodFacts"_

This project is done as part of the course “Développeur d'application - Python”
from the online training platform OpenClassrooms.
[Project 5](https://openclassrooms.com/fr/projects/157/assignment)

>__Project's objective__
>
>Build a python's application which interact with a MySQL database and an API.

## What it should do

The user selects a product from the Open Food Facts database and the program
return a substitute which can be saved by the user.

* Select a category
* Select a product
* The program offers a substitute and shows its description and a store where buy it
* The user has the possibility to save the result
## Requests API OFF (Open Food Fact)

Make use of library requests.py to get the list of products from OFF.

### _multirequest()_
To retrieve data of many products we use a
[Search Requests](https://documenter.getpostman.com/view/8470508/SVtN3Wzy#58efae40-73c3-4907-9a88-785faff6ffb1)

search_url = https://world.openfoodfacts.org/cgi/search.pl?

We only need to set the number of product and from which category it come from.

For the number we use page_size and for the category we use the parameter
criteria with the tag category
(tagtype_0=categories&tag_contains_0=contains&tag_0= xxx).

Parameter are the categories weight (dictionary) and an int for the number of product, by default it take it from setting.json.
It returns a list of products (list[dictionary]).

### _unirequest()_
retrieve data of one specific products WIP

## Products treatment
When retrieved for the API OFF product need to be stocked in data base and python need to be able to use it.

### _intoproduct()_
Convert the dictionary given by OFF into a Product.
It will only conserve the following attribute:
* product_name
* categories
* origins
* labels
* additives
* ingredients
* stores
* nova_groups
* nutrition_score

Parameter is a product dictionary and it returns a Product.

### _insertproduct()_
Use of SQLAlchemy to insert product in DB