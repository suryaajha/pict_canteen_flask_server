from flask import Flask
from flask import jsonify, request

from modal import FoodItem, Order, User
from modal import StatusMessage, Document
import traceback as tb
import json

import constants 

import pymongo

import uuid

username = 'backend_server'
password = 'backend_server'

mongo_uri = 'mongodb://' + username + ':' + password + '@pictmesscluster-shard-00-00-p2qbv.mongodb.net:27017,pictmesscluster-shard-00-01-p2qbv.mongodb.net:27017,pictmesscluster-shard-00-02-p2qbv.mongodb.net:27017/test?ssl=true&replicaSet=pictmesscluster-shard-0&authSource=admin&retryWrites=true'

client = pymongo.MongoClient(mongo_uri)
db = client.pict_canteen

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

@app.route('/populate/add_food_item', methods = ['GET','POST'])
def add_food_item():
	error = 'Error Message'

	try:
		if request.method == 'POST':
			new_food_document = {
				constants.FOOD._ID : str(uuid.uuid4()),
				constants.FOOD.NAME : request.form.get('name'),
				constants.FOOD.PRICE : request.form.get('price'),
				constants.FOOD.DESCRIPTION : request.form.get('description'),
				constants.FOOD.IMAGE_URL : request.form.get('image_url'),
				constants.FOOD.SECTION : request.form.get('section')
			}
			print(new_food_document['image_url'])
			# Once food item is ready push to database
			inserted_id = db.food.insert_one(new_food_document).inserted_id
			statusMessage = StatusMessage(code = 200, message = 'Successfully inserted document with id ' + str(inserted_id))
			return statusMessage.jsonify()

	except Exception as e:
		print(e)
		tb.print_exc()
		return error

"""
	items key should give give string version of json like this
	"{'key' : 'value' , 'key2' : 'value2'}"
"""
@app.route('/populate/add_order_item', methods = ['GET','POST'])
def add_order_item():
	error = 'Error Message'

	try:
		if request.method == 'POST':
			order = Order(
				request.args.get('recipient_id'),
				request.args.get('total_amt'),
				request.args.get('timestamp'),
				request.args.get('items_json')
				)
			# Once food item is ready push to database
			inserted_id = db.users.insert_one(order.dictify()).inserted_id
			statusMessage = StatusMessage(code = 200, message = 'Successfully inserted document with id ' + str(inserted_id))
			return statusMessage.jsonify()

	except Exception as e:
		print(e)
		tb.print_exc()
		return error

@app.route('/populate/add_user_item', methods = ['GET','POST'])
def add_user_item():
	error = 'Error Message'

	try:
		if request.method == 'POST':
			user = User(
				request.args.get('name'),
				request.args.get('reg_id'),
				request.args.get('contact_no'),
				request.args.get('photo_url')
				)
			# Once food item is ready push to database
			inserted_id = db.users.insert_one(user.dictify()).inserted_id
			statusMessage = StatusMessage(code = 200, message = 'Successfully inserted document with id ' + str(inserted_id))
			return statusMessage.jsonify()

	except Exception as e:
		print(e)
		tb.print_exc()
		return error


@app.route('/rest/get_food_details', methods = ['GET'])
def get_food_details():
	error = 'Error Message'

	try:
		if request.method == 'GET':
			section = request.args.get('section')
			print("Parameter Rec : " + str(section))
			food_list = [] 
			for food in db.food.find():
				food_list.append(food)
			return json.dumps(food_list)

	except Exception as e:
		print(e)
		tb.print_exc()
		return error

@app.route('/rest/get_food_details_with_id', methods = ['GET'])
def get_food_details_with_id():
	error = 'Error Message'

	try:
		if request.method == 'GET':
			food_id = request.args.get('food_id')
			food_list = [] 
			for food in  db.food.find({
					constants.FOOD._ID : food_id
				}):
				food_list.append(food)
			return json.dumps(food_list)

	except Exception as e:
		print(e)
		tb.print_exc()
		return error

@app.route('/auth/signin', methods = ['GET'])
def signin():
	error = 'Error Message'

	try:
		if request.method == 'GET':
			user_id = request.args.get('user_id')
			password = request.args.get('password')
			user_document = db[constants.COLLECTION_NAMES.USERS].find_one({
					'reg_id' : user_id
				})
			if user_document == None:
				statusMessage = StatusMessage(code = constants.AUTH.NO_USER, message = "Invalid Username")
				return statusMessage.jsonify_attr()

			if password == user_document[constants.USERS.PASSWORD]:
				statusMessage = StatusMessage(code = constants.AUTH.SUCCESS, message = 'Successfully Verified Account', id = user_document[constants.USERS.REG_ID])
				return statusMessage.jsonify_attr()
			else:
				statusMessage = StatusMessage(code = constants.AUTH.FAILURE, message = "Username and password don't match")
				return statusMessage.jsonify_attr()

	except Exception as e:
		print(e)
		tb.print_exc()
		return error

@app.route('/auth/signup', methods = ['POST'])
def signup():
	error = 'Error Message'

	try:
		if request.method == 'POST':
			new_user_document = {
				constants.USERS._ID : request.form.get('reg_id'),
				constants.USERS.NAME : request.form.get('name'),
				constants.USERS.REG_ID : request.form.get('reg_id'),
				constants.USERS.PASSWORD : request.form.get('password'),
				constants.USERS.CONTACT_NO : request.form.get('contact_no'),
				constants.USERS.PHOTO_URL : request.form.get('photo_url')
			}

			user_document = db[constants.COLLECTION_NAMES.USERS].find_one({
					'reg_id' : request.form.get('reg_id')
				})

			if user_document != None:
				statusMessage = StatusMessage(code = constants.AUTH.FAILURE, message = "Account already exist with this user id. Please try to login!")
				return statusMessage.jsonify_attr()

			inserted_id = db[constants.COLLECTION_NAMES.USERS].insert_one(new_user_document).inserted_id
			statusMessage = StatusMessage(code = constants.AUTH.SUCCESS, message = "Account Created Successfully", user_id = str(inserted_id))
			return statusMessage.jsonify_attr()			

	except Exception as e:
		print(e)
		tb.print_exc()
		return error

@app.route('/auth/user', methods = ['GET'])
def get_user():
	error = 'Error Message'

	try:
		if request.method == 'GET':
			user_id = request.args.get('user_id')
			user_document = db[constants.COLLECTION_NAMES.USERS].find_one({
					'reg_id' : user_id
				})
			print(user_document)
			if user_document == None:
				statusMessage = StatusMessage(code = constants.AUTH.NO_USER, message = "Invalid Username")
				return statusMessage.jsonify_attr()
			else:
				user = Document(user_document)
				return user.jsonify_attr()

	except Exception as e:
		print(e)
		tb.print_exc()
		return error

@app.route('/transaction', methods = ['POST'])
def transaction():
	error = 'Error Message'

	try:
		if request.method == 'POST':
			new_user_document = {
				constants.TRANSACTION._ID : str(uuid.uuid4()),
				constants.TRANSACTION.RECIPIENT_ID : request.form.get('recipient_id'),
				constants.TRANSACTION.ITEMS : request.form.get('items'),
				constants.TRANSACTION.TOTAL_AMT : request.form.get('total_amt'),
				constants.TRANSACTION.PAYMENT_METHOD : request.form.get('payment_method'),
				constants.TRANSACTION.TRANSACTION_TIME : request.form.get('transaction_time')
			}

			transaction_id = db[constants.COLLECTION_NAMES.ORDERS].insert_one(new_user_document).inserted_id
			statusMessage = StatusMessage(code = constants.TRANSACTION.SUCCESS, message = "Transaction Processed Successfully", transaction_id = str(transaction_id))
			return statusMessage.jsonify_attr()			

	except Exception as e:
		print(e)
		tb.print_exc()
		statusMessage = StatusMessage(code = constants.TRANSACTION.FAILURE, message = "Transaction Failed", user_id = str(0000))
		return statusMessage.jsonify_attr()		


if __name__ == '__main__':
	# Uncomment below to use in production
	app.run(host= '0.0.0.0',port=8080,debug=True)
	#app.run(debug=True)
