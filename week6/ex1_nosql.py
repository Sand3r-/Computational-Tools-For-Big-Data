from pymongo import MongoClient

def debpr(collection):
    for entity in collection:
        print(entity["ProductName"], entity[""])


client = MongoClient('localhost', 27017)
db = client.Northwind

customer_id = "ALFKI"

orders = db['orders'].find({"CustomerID" : customer_id})

for order in orders:
    details = db['order-details'].find({"OrderID" : order["OrderID"]})
    for detail in details:
        products = db['products'].find({"ProductID" : detail["ProductID"]})
        for product in products:
            print(product["ProductID"], product["ProductName"])



# print(len(product_id_list))
# print(product_id_list)

# products = db['products'].find({"ProductID" : {"$in" : product_id_list}})
# print(len(pro))

# for product in products:
#     print(product["ProductID"], product["ProductName"])