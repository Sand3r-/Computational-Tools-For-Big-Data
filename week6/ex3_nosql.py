from pymongo import MongoClient

def debpr(collection):
    for entity in collection:
        print(entity["ProductName"], entity[""])


client = MongoClient('localhost', 27017)
print(client.database_names())
db = client.Northwind
print(db.collection_names())

suppliers = db['suppliers'].find()

number_of_inter_disc_suppliers = 0
for supplier in suppliers:
    products = db['products'].find({"SupplierID" : supplier["SupplierID"]})
    different_categories_num = len(products.distinct("CategoryID")) 
    if different_categories_num >= 2 and different_categories_num <= 4:
        number_of_inter_disc_suppliers += 1

print(number_of_inter_disc_suppliers)
    # print(supplier["SupplierID"], len(products.distinct("CategoryID")))
    # for product in products.distinct("CategoryID"):
    #     print(supplier["SupplierID"], product)