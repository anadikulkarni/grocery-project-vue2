from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash
from flask_cors import CORS

# Redis and Celery for batch jobs/caching
# edit product default mfd not showing

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"], 
     methods=["GET", "POST"], 
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"], 
     supports_credentials=True)

with open('config.json') as config_file:
    config_data = json.load(config_file)

app.config['SECRET_KEY'] = config_data['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config_data['SQLALCHEMY_DATABASE_URI']
app.config['MAIL_SERVER'] = config_data['MAIL_SERVER']
db = SQLAlchemy(app)

admin_creds = {'username' : 'admin',
               'password': 'password'}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if Manager.query.get(int(user_id)):
        return Manager.query.get(int(user_id))
    elif User.query.get(int(user_id)):
        return User.query.get(int(user_id))
    return None

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    is_authenticated = db.Column(db.Boolean(), nullable = False, default = False)
    
class Manager(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), unique = True, nullable = False)
    products = db.relationship("Product", backref="category", lazy=True, cascade = "all, delete")
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'products': [product.as_dict() for product in self.products]
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    productName = db.Column(db.String(100), nullable = False)
    unit = db.Column(db.String(100), nullable = False)
    rateUnit = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    categoryid = db.Column(db.Integer, db.ForeignKey("category.id"), nullable = False)
    cartitem = db.relationship("CartItem", backref="product", lazy=True)
    mfd = db.Column(db.DateTime, nullable = False)
    def as_dict(self):
        return {
            'id': self.id,
            'productName': self.productName,
            'unit': self.unit,
            'rateUnit': self.rateUnit,
            'quantity': self.quantity,
            'categoryid': self.categoryid,
            'cartitem': [cart_item.as_dict() for cart_item in self.cartitem],
            'mfd': self.mfd,
        }
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable = False)
    productid = db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False)
    productName = db.Column(db.String(100), nullable = False)
    unit = db.Column(db.String(100), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    rateUnit = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(100), nullable = False)
    def as_dict(self):
        return {
        'id': self.id,
        'userid': self.userid,
        'productid': self.productid,
        'productName': self.productName,
        'unit': self.unit,
        'quantity': self.quantity,
        'rateUnit': self.rateUnit,
        'category': self.category,
    }
    
class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable = False)
    productid = db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False)
    productName = db.Column(db.String(100), nullable = False)
    unit = db.Column(db.String(100), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    rateUnit = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(100), nullable = False)
    purchaseDate = db.Column(db.DateTime, default = datetime.utcnow)
    
class ApprovalRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(100))
    category = db.Column(db.String(50), nullable=True)
    action = db.Column(db.String(50), nullable=True)
    categoryID = db.Column(db.Integer, nullable=True)

    def _repr_(self):
        return f"ApprovalRequest('{self.username}', '{self.category}', '{self.action}')"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    is_manager = data['isManager']
    existing_user = User.query.filter_by(username=username).first()
    existing_manager = Manager.query.filter_by(username=username).first()
    existing_manager_request = ApprovalRequest.query.filter_by(username=username, category='manager').first()

    if existing_user or existing_manager or existing_manager_request:
        return jsonify({"message": "Username already taken!"}), 400

    if is_manager:
        approval_request = ApprovalRequest(username=username, password=password, email=email, category="manager", action="registration")
        db.session.add(approval_request)
    else:
        user = User(username=username, password=password, email=email)
        db.session.add(user)

    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 200

@app.route('/manager_login', methods=['POST'])
def manager_login():
    data = request.json
    username = data['username']
    password = data['password']
    current_user = User.query.filter_by(username=username).first()
    manager = Manager.query.filter_by(username=username).first()
    if manager:
        if current_user and current_user.is_authenticated:
            return jsonify({"message": "Already logged in", "status": "success"}), 200
        if current_user and current_user.password == password:
            current_user.is_authenticated = True
            db.session.commit()
            return jsonify({"message": "Login successful!", "status": "success"}), 200
        else:
            return jsonify({"message": "Login failed. Invalid credentials.", "status": "fail"}), 401
    else:
        return jsonify({"message": "Invalid manager", "status": "fail"}), 404
    
@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.json
    username = data['username']
    password = data['password']
    current_user = User.query.filter_by(username=username).first()
    if current_user:
        if username == admin_creds["username"] and password == admin_creds["password"]:
            current_user.is_authenticated = True
            db.session.commit()
            return jsonify({"message": "Login successful!", "status": "success"}), 200
        else:
            return jsonify({"message": "Login failed. Invalid credentials.", "status": "fail"}), 401
    else:
        current_user = User(username = username, password = password, email = "admin@admin.com", is_authenticated = True)
        if username == admin_creds["username"] and password == admin_creds["password"]:
            db.session.add()
            db.session.commit()
            return jsonify({"message": "Login successful!", "status": "success"}), 200

        else:
            return jsonify({"message": "Login failed. Invalid credentials.", "status": "fail"}), 401
        
@app.route('/user_login', methods=['POST'])
def user_login():
    data = request.json
    username = data['username']
    password = data['password']
    current_user = User.query.filter_by(username=username).first()
    if current_user and current_user.is_authenticated:
        return jsonify({"message": "Already logged in", "status": "success"}), 200
    if current_user and current_user.password == password:
        current_user.is_authenticated = True
        db.session.commit()
        return jsonify({"message": "Login successful!", "status": "success"}), 200
    else:
        return jsonify({"message": "Login failed. Invalid credentials.", "status": "fail"}), 401

@app.route('/logout')
def logout():
    username = request.args.get("username", None)
    current_user = User.query.filter_by(username=username).first()
    current_user.is_authenticated = False
    db.session.commit()
    return jsonify({"message": "Logout successful!", "status": "success"}), 200

@app.route('/pending_requests', methods=['GET'])
def pending_requests():
    username = request.args.get('username', None)
    current_user = User.query.filter_by(username = username).first()
    requests = ApprovalRequest.query.all()
    if current_user and username == admin_creds['username']:
        if current_user.is_authenticated:
            categories = Category.query.all()
            category_list = [category.as_dict() for category in categories if category]
            return jsonify({
                "categories": category_list, 
                'admin': username, 
                'requests':  [{'id':pending.id, 
                               'action': pending.action.replace("_", " ").capitalize(),
                               'username':pending.username, 
                               'category': pending.category} for pending in requests],
                }
                )
        else:
            logout_user()
            return jsonify({"categories": None, "manager": None}), 401
    else:
        return jsonify({"categories": None, "manager": None}), 404

@app.route('/approve-request/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    request_to_approve = ApprovalRequest.query.get(request_id)
    if not request_to_approve:
        return jsonify({"message": "Request not found", "status": "fail"}), 404
    if request_to_approve.category == "manager":
        new_manager = Manager(username=request_to_approve.username, password=request_to_approve.password, email=request_to_approve.email)
        new_manager_user = User(username=request_to_approve.username, password=request_to_approve.password, email=request_to_approve.email)
        db.session.add(new_manager)
        db.session.add(new_manager_user)      
        db.session.delete(request_to_approve)      
        db.session.commit()
        return jsonify({"message": "Manager approved and added", "status": "success"}), 200
    if request_to_approve.action == "create_category":
        category_name = request_to_approve.category
        if not category_name:
            return jsonify({'status': 'fail', 'message': 'Category name is required'}), 400
        new_category = Category(name=category_name)
        try:
            db.session.add(new_category)
            db.session.delete(request_to_approve)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Category saved successfully'})
        except Exception as e:
            print(e)
            return jsonify({'status': 'fail', 'message': 'An error occurred: ' + str(e)}), 500
    if  request_to_approve.action == "edit_category":
        category_name = request_to_approve.category
        categoryID = request_to_approve.categoryID
        if not category_name:
            return jsonify({'status': 'fail', 'message': 'Category name is required'}), 400
        try:
            category = Category.query.get(categoryID)
            if not category:
                return jsonify({'status': 'error',
                    'message': 'category not found'}), 404
            category.name = category_name
            db.session.commit()
            return jsonify({'status':'success',
                            'message':'category saved successfully'})
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({'status':'error',
                            'message':f'an error occurred: {str(e)}'}), 500  
    if  request_to_approve.action == "delete_category":
        categoryID = request_to_approve.categoryID
        if not categoryID:
            return jsonify({'status': 'fail', 'message': 'Category ID is required'}), 400
        try:
            category = Category.query.get(categoryID)
            if not category:
                return jsonify({'status': 'error',
                    'message': 'category not found'}), 404
            db.session.delete(category)
            db.session.commit()
            return jsonify({'status':'success',
                            'message':'category deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status':'error',
                            'message':f'an error occurred: {str(e)}'}), 500
    return jsonify({"message": "Request type not handled", "status": "fail"}), 400

@app.route('/decline-request/<int:request_id>', methods=['POST'])
def decline_request(request_id):
    request_to_approve = ApprovalRequest.query.get(request_id)
    if not request_to_approve:
        return jsonify({"message": "Request not found", "status": "fail"}), 404
    try:
        db.session.delete(request_to_approve)
        db.session.commit()
        return jsonify({
            'message' : "Request deleted successfully",
            'status' : 'success',
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500

@app.route('/categories', methods=['GET'])
def category():
    username = request.args.get("username", default=None)
    current_user = User.query.filter_by(username=username).first()
    manager = Manager.query.filter_by(username=username).first()
    if manager:
        if (current_user.is_authenticated):
            categories = Category.query.all()
            category_list = [category.as_dict() for category in categories if category]
            return jsonify({"categories": category_list, "manager": username})
        else:
            logout_user()
            return jsonify({"message": "Manager not authenticated", "status": "fail"}), 401
    else:
        return jsonify({"message": "Invalid manager", "status": "fail"}), 404
    
@app.route('/categories_user', methods=['GET'])
def category_user():
    username = request.args.get("username", default=None)
    current_user = User.query.filter_by(username=username).first()
    if (current_user.is_authenticated):
        categories = Category.query.all()
        category_list = [category.as_dict() for category in categories if category]
        return jsonify({"categories": category_list, "user": username})
    else:
        logout_user()
        return jsonify({"message": "User not authenticated", "status": "fail"}), 401

@app.route('/save_category', methods=['POST'])
def save_category():
    data = request.json
    categoryName = data.get("category_name")
    if not categoryName:
        return jsonify({'status': 'error',
                        'message': 'category name is required'}), 400
    new_category = Category(name=categoryName)
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'category saved successfully'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/update_category', methods=['POST'])
def update_category():
    data = request.json
    categoryID = data.get("id")
    categoryName = data.get("name")
    try:
        category = Category.query.get(categoryID)
        if not category:
            return jsonify({'status': 'error',
                'message': 'category not found'}), 404
        category.name = categoryName
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'category saved successfully'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/delete_category', methods=['POST'])
def delete_category():
    data = request.json
    categoryID = data.get("categoryID")
    try:
        category = Category.query.get(categoryID)
        if not category:
            return jsonify({'status': 'error',
                'message': 'category not found'}), 404
        db.session.delete(category)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'category deleted successfully'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/create_category_request', methods=['POST'])
def create_category_request():
    data = request.json
    username = data['username']
    category = data['category']
    existing_manager = Manager.query.filter_by(username=username).first()
    if existing_manager:
        approval_request = ApprovalRequest(username=username, category=category, action="create_category")
        db.session.add(approval_request)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'category create request sent successfully'})
    else:
        return jsonify({'status': 'error',
                        'message': 'category create request failed'})
        
@app.route('/edit_category_request', methods=['POST'])
def edit_category_request():
    data = request.json
    username = data['username']
    category = data['category']
    categoryID = data['categoryID']
    existing_manager = Manager.query.filter_by(username=username).first()
    if existing_manager:
        approval_request = ApprovalRequest(username=username, category=category, action="edit_category", categoryID=categoryID)
        db.session.add(approval_request)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'category edit request sent successfully'})
    else:
        return jsonify({'status': 'error',
                        'message': 'category edit request failed'})
        
@app.route('/delete_category_request', methods=['POST'])
def delete_category_request():
    data = request.json
    username = data['username']
    categoryID = data['categoryID']
    existing_manager = Manager.query.filter_by(username=username).first()
    if existing_manager:
        approval_request = ApprovalRequest(username=username, action="delete_category", categoryID=categoryID)
        db.session.add(approval_request)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'category delete request sent successfully'}), 200
    else:
        return jsonify({'status': 'error',
                        'message': 'category delete request failed'}), 401
        
@app.route('/save_product', methods=['POST'])
def save_product():
    data = request.json
    categoryid = data.get("categoryid")
    productName = data.get("productName")
    unit = data.get("unit")
    rateUnit = data.get("rateUnit")
    quantity = data.get("quantity")
    mfd = datetime.strptime(data.get("mfd"), "%Y-%m-%d")
    category = Category.query.get(categoryid)
    if not productName:
        return jsonify({'status': 'error',
                        'message': 'product name is required'}), 400
    new_product = Product(category=category, productName=productName, unit=unit, rateUnit=rateUnit, quantity=quantity, mfd=mfd)
    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'product saved successfully'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/edit_product', methods=['POST'])
def edit_product():
    data = request.json
    productID = data.get("productId")
    productName = data.get("productName")
    unit = data.get("unit")
    rateUnit = data.get("rateUnit")
    quantity = data.get("quantity")
    mfd = datetime.strptime(data.get("mfd"), "%Y-%m-%d")
    product = Product.query.get(productID)
    if not product:
        return jsonify({'status': 'error',
                        'message': 'product not found'}), 404
    product.productName = productName
    product.unit = unit
    product.rateUnit = rateUnit
    product.quantity = quantity
    product.mfd = mfd
    try:
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'product edited successfully'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.json
    productID = data.get("productID")
    try:
        product = Product.query.get(productID)
        if not product:
            return jsonify({'status': 'error',
                'message': 'product not found'}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':'product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/cart')
def cart():
    username = request.args.get("username", default=None)
    current_user = User.query.filter_by(username=username).first()
    if (current_user.is_authenticated):
        items = CartItem.query.filter_by(userid = current_user.username).all()
        items_list = [items.as_dict() for items in items if items]
        return jsonify({"items": items_list, "user": username})
    else:
        logout_user()
        return jsonify({"message": "User not authenticated", "status": "fail"}), 401
    
@app.route('/remove_item', methods=['POST'])
def remove_item():
    data = request.json
    itemid = data.get("itemID")
    try:
        cartitem = CartItem.query.get(itemid)
        quantity = cartitem.quantity
        productid = cartitem.productid
        product = Product.query.get(productid)
        if not product:
            return jsonify({'status': 'error',
                'message': 'product not found'}), 404
        if product.quantity < quantity:
            return jsonify({'status':'success',
                'message':f'not enough stock, remaining quantity: {product.quantity}'})

        product.quantity += quantity
        db.session.delete(cartitem)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':f'product removed from cart successfully, remaining quantity: {product.quantity}'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500

@app.route('/add_to_cart_product', methods=['POST'])
def add_to_cart_product():
    data = request.json
    productID = data.get("productID")
    quantity = int(data.get("quantity"))
    userID = data.get("username")
    try:
        product = Product.query.get(productID)
        productName = product.productName
        unit = product.unit
        rateUnit = product.rateUnit
        category = product.category.name
        cartitem = CartItem(userid=userID, productName=productName, productid=productID, unit=unit,
                            quantity=quantity, rateUnit=rateUnit, category = category)
        if not product:
            return jsonify({'status': 'success',
                'message': 'product not found'}), 404
        if product.quantity < quantity:
            return jsonify({'status':'success',
                'message':f'not enough stock, remaining quantity: {product.quantity}'})

        product.quantity -= quantity
        db.session.add(cartitem)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':f'product added to cart successfully, remaining quantity: {product.quantity}'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/purchase_product', methods=['POST'])
def purchase_product():
    data = request.json
    productID = data.get("productID")
    quantity = int(data.get("quantity"))
    userID = data.get("username")
    try:
        product = Product.query.get(productID)
        productName = product.productName
        unit = product.unit
        rateUnit = product.rateUnit
        category = product.category.name
        ledger = Ledger(userid=userID, productName=productName, productid=productID, unit=unit,
                            quantity=quantity, rateUnit=rateUnit, category = category)
        if not product:
            return jsonify({'status': 'error',
                'message': 'product not found'}), 404
        if product.quantity < quantity:
            return jsonify({'status':'success',
                'message':f'not enough stock, remaining quantity: {product.quantity}'})

        product.quantity -= quantity
        db.session.add(ledger)
        db.session.commit()
        return jsonify({'status':'success',
                        'message':f'product purchased successfully, remaining quantity: {product.quantity}'})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status':'error',
                        'message':f'an error occurred: {str(e)}'}), 500
        
@app.route('/buy_all', methods = ['POST'])
def buy_all():
    data = request.get_json()
    username = data['userID']
    current_user = User.query.filter_by(username=username).first()
    if (current_user.is_authenticated):
        try:
            cart_items = CartItem.query.filter_by(userid = username).all()
            for item in cart_items:
                ledger = Ledger(userid=item.userid, productName=item.productName, productid=item.productid, unit=item.unit,
                                quantity=item.quantity, rateUnit=item.rateUnit, category = item.category)
                db.session.add(ledger)
                db.session.delete(item)
            db.session.commit()
            return jsonify({'status':'success',
                            'message':f'products bought successfully'})
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({'status':'error',
                            'message':f'an error occurred: {str(e)}'}), 500
    else:
        logout_user()
        return jsonify({'status': 'error',
            "message": "User not authenticated", "status": "fail"}), 401        

with app.app_context():
   db.create_all()
   
if __name__ == "__main__":
    app.run(debug=True)