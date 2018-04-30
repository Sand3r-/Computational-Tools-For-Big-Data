from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.Northwind

customer_id = "ALFKI"
orders = db['orders'].find({"CustomerID" : customer_id})

print("OrderID\t ProductID\t CategoryID\t ProductName")
for order in orders:
    saved_orders = []
    details = db['order-details'].find({"OrderID" : order["OrderID"]})
    categories = []
    for detail in details:
        products = db['products'].find({"ProductID" : detail["ProductID"]})
        for product in products:
            if product["CategoryID"] not in categories:
                categories.append(product["CategoryID"])
            saved_orders.append((order["OrderID"], product["ProductID"], 
                product["CategoryID"], product["ProductName"]))
    if len(categories) > 1:
        for order_id, product_id, category_id, product_name in saved_orders:
            print(order_id, '\t', product_id, '\t\t', category_id, '\t\t', product_name)
        # print(list(products))

    #     overall_products = overall_products + list(products)
    # overall_products = Cursor(overall_products)
    # number_of_categories = len(products.distinct("CategoryID"))
    # print(products.distinct("CategoryID"))
    # if number_of_categories > 1:
    #     for product in products:
    #         print(order["OrderID"], product["ProductID"], product["ProductName"])
