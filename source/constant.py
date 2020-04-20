# Default preference

PREF = {
    'equal product': 0.9,
    'score weight': [
        'nutriscore',
        'labelscore',
        'nova'
    ],
    'categories weight': {
        'Plant-based foods and beverages': 22,
        'Plant-based foods': 19,
        'Snacks': 10,
        'Beverages': 9,
        'Sweet snacks': 8,
        'Dairies': 8,
        'Fruits and vegetables based foods': 6,
        'Cereals and potatoes': 6,
        'Meats': 6,
        'Fermented foods': 5,
        'Fermented milk products': 5,
        'Meals': 5,
        'Groceries': 4,
        'Spreads': 4,
        'Biscuits and cakes': 4,
        'Cereals and their products': 4,
        'Cheeses': 3,
        'Breakfasts': 3,
        'Prepared meats': 3,
        'Plant-based beverages': 3,
        'Fruits based foods': 3,
        'Sauces': 3,
        'Desserts': 3,
        'Vegetables based foods': 2,
        'Seafood': 2,
        'Sweet spreads': 2,
        'Confectioneries': 2,
        'Canned foods': 2,
        'Frozen foods': 2,
        'Plant-based spreads': 2,
        'Fishes': 2,
        'Biscuits': 1,
        'Alcoholic beverages': 1,
        'Fats': 1,
        'Salty snacks': 1,
        'Fruit-based beverages': 1,
        'Chocolates': 1,
        'Yogurts': 1,
        'Condiments': 1,
        'Breads': 1,
        'Juices and nectars': 1,
        'Poultries': 1,
        'Legumes and their products': 1,
        'Appetizers': 1,
        'Nuts and their products': 1,
        'Meat-based products': 1,
        'Seeds': 1,
        'Dried products': 1,
        'Fruit preserves': 1,
        'Cakes': 1,
        'Vegetable fats': 1,
        'Canned plant-based foods': 1,
        'Sweetened beverages': 1,
        'Sweeteners': 1,
        'Cow cheeses': 1,
        'Jams': 1,
        'Fruit juices': 1,
        'French cheeses': 1,
        'Fresh foods': 1,
        'Olive tree products': 1,
        'Salted spreads': 1,
        'Vegetable oils': 1,
        'Pastas': 1,
        'Legumes': 1,
        'Hot beverages': 1,
        'Chickens': 1,
        'Meals with meat': 1,
        'Fruit jams': 1,
        'Farming products': 1
    }
}

# Seize sample
SEIZE_SAMPLE = 200

# Engine dbase
user = 'root'
password = 'vi19sa96&*'
port = '3305'
ENGINE = 'mysql://' + user + ':' + password + 'Mysql@localhost:' + port
DBASE = 'OpenFoodFact'

bgcolor = '#d9d9d9'  # X11 color: 'gray85'
fgcolor = '#000000'  # X11 color: 'black'
compcolor = '#d9d9d9'  # X11 color: 'gray85'
ana1color = '#d9d9d9'  # X11 color: 'gray85'
ana2color = '#ececec'  # Closest X11 color: 'gray92'
