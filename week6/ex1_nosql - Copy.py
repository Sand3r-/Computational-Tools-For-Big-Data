from pymongo import MongoClient

def debpr(collection):
    for entity in collection:
        print(entity["ProductName"], entity[""])


client = MongoClient('localhost', 27017)
print(client.database_names())
db = client.Northwind
print(db.collection_names())

customer_id = "ALFKI"

orders = db['orders'].find({"CustomerID" : customer_id})
order_id_list = [order["OrderID"] for order in orders]
print(len(order_id_list))

for order_id in order_id_list:
    detail = db['order-details'].find({"OrderID" : order_id})
    print(detail[0])

# details = db['order-details'].find({"OrderID" : {"$in" : order_id_list}})
# product_id_list = [detail["ProductID"] for detail in details]
# print(len(product_id_list))
# print(product_id_list)

# products = db['products'].find({"ProductID" : {"$in" : product_id_list}})
# print(len(pro))

# for product in products:
#     print(product["ProductID"], product["ProductName"])