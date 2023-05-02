from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response

import database as db
import authentication
import ordermanagement as om
import pymongo
import logging
from flask import flash
from flask import Flask, render_template, redirect, url_for, request
import database as db

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'
client = pymongo.MongoClient("mongodb://localhost:27017/")
db3 = client.order_management

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)



@app.route('/')
def index():
    return render_template('index.html', page="Index")



@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches",branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))

    return render_template('branchdetails.html', code=code, branch=branch)
def get_branch_details(code):
    branch = db.get_branch(code)
    return branch


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    return render_template('login.html')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    error = None
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    elif db.get_user(username) == None and password != "Ch@ng3m3!":
        error = "Incomplete login data is passed"
    elif db.get_user(username) == None:
        error = "Username entered is invalid"
    elif password != "Ch@ng3m3!":
        error = "Incorrect password"
    else:
        error = "Invalid"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')


@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a 
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

#@app.route('/updatecart', methods=['POST'])
#def update_cart():
#    item_codes = request.form.getlist('item_code[]')
#    item_quantities = request.form.getlist('item_qty[]')
#    for code, qty in zip(item_codes, item_quantities):
#        cart.update_item(code, int(qty))
#    return redirect('/cart')
@app.route('/updatecart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    for item_id in request.form:
        cart[item_id]['qty'] = int(request.form[item_id])
        cart[item_id]['subtotal'] = cart[item_id]['price'] * cart[item_id]['qty']
    session['cart'] = cart
    return redirect('/cart')



@app.route("/cart/remove/<item_id>", methods=['POST'])
def remove_from_cart(item_id):
    cart = ShoppingCart.remove(item_id)
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/orders')
def orders():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']['username']
    orders = db3.orders.find({'username': username})
    if orders.count() == 0:
        return render_template('no_orders.html')
    else:
        return render_template('orders.html', orders=orders)

@app.route('/api/products',methods=['GET'])
def api_get_products():
    resp = make_response( dumps(db.get_products()) )
    resp.mimetype = 'application/json'
    return resp
@app.route('/api/products/<int:code>',methods=['GET'])
def api_get_product(code):
    resp = make_response(dumps(db.get_product(code)))
    resp.mimetype = 'application/json'
    return resp
