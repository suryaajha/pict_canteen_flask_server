import json
import ast

class Modal():

	def dictify(self):
		# converts string representation of dict to dict object using ast module
		data = ast.literal_eval(self.jsonify())
		return data

	def jsonify(self):
		return json.dumps(self.__dict__)

	def jsonify_attr(self):
		return json.dumps(self.attr)

	def set_message(self, message):
		self.is_message = True
		self.message = message

class FoodItem(Modal):
	def __init__(self, section, name, price, description, image_url):
		super(FoodItem, self).__init__()
		self.section = section
		self.name = name
		self.price = price
		self.description = description
		self.image_url = image_url

class User(Modal):
	"""docstring for User"""
	def __init__(self, name, reg_id, contact_no, photo_url):
		super(User, self).__init__()
		self.name = name
		self.reg_id = reg_id
		self.contact_no = contact_no
		self.photo_url = photo_url

class Order(Modal):
	"""docstring for Order"""
	def __init__(self, recipient_id, total_amt, timestamp, items):
		super(Order, self).__init__()
		self.recipient_id = recipient_id
		self.total_amt = total_amt
		self.timestamp = timestamp
		# convert string representation of items dict to dict 
		self.items = ast.literal_eval(items)

	def dictify(self):
		data =  {
			'recipient_id' : self.recipient_id,
			'total_amt' : self.total_amt,
			'timestamp' : self.timestamp,
			'items' : self.items
		}
		return data

class StatusMessage(Modal):
	"""docstring for StatusMessage"""
	def __init__(self, **kwargs):
		super(StatusMessage, self).__init__()
		self.attr = dict()
		for key, value in kwargs.items():
			self.attr[key] = value
		
class Document(Modal):
	"""docstring for StatusMessage"""
	def __init__(self, **kwargs):
		super(Document, self).__init__()
		self.attr = dict()
		for key, value in kwargs.items():
			self.attr[key] = value

	def __init__(self, dictionary):
		self.attr = dictionary