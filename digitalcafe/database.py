import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]
order_management_db = myclient["order_management"]
branches_db = myclient["branches"]





branches = {
    1: {"name":"Katipunan"},
    2: {"name":"Tomas Morato"},
    3: {"name":"Eastwood"},
    4: {"name":"Tiendesitas"},
    5: {"name":"Arcovia"},
}


def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user



def get_product(code):
    products_coll = products_db["products"]

    product = products_coll.find_one({"code":code},{"_id":0})

    return product

def get_products():
    product_list = []

    products_coll = products_db["products"]

    for p in products_coll.find({},{"_id":0}):
        product_list.append(p)


def get_branch(code):
    branches_coll = branches_db["branches"]

    branch= branches_coll.find_one({"code":code})

    return branch


def get_branches():
    branch_list = []


    branches_coll = branches_db["branches"]

    for p in branches_coll.find({}):
        branch_list.append(p)


    return branch_list


def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)


