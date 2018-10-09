BREAKFAST = "breakfast"
LUNCH = "dinner"

"""
	Collection Names
"""
class COLLECTION_NAMES:
	USERS  = "users"
	FOOD = "food"
	ORDERS = "orders"

class USERS :
	REG_ID = 'reg_id'
	PASSWORD = 'password'
	CONTACT_NO = 'contact_no'
	PHOTO_URL = 'photo_url'
	NAME = 'name'
	_ID = '_id'

class AUTH :
	SUCCESS =  200
	FAILURE = 404
	NO_USER = 111
	
class FOOD:
	_ID = '_id'
	NAME = 'name'
	PRICE = 'price'
	DESCRIPTION = 'description'
	IMAGE_URL = 'image_url'
	SECTION = 'section'

class TRANSACTION:
	_ID = '_id'
	RECIPIENT_ID = 'recipient_id'
	ITEMS = 'items'
	TOTAL_AMT = 'total_amt'
	PAYMENT_METHOD = 'payment_method'
	TRANSACTION_TIME = 'transaction_time'
	SUCCESS =  200
	FAILURE = 404